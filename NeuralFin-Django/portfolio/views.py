from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Portfolio, PortfolioItem
from .serializers import PortfolioSerializer, PortfolioItemSerializer

class PortfolioListCreateView(generics.ListCreateAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PortfolioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class PortfolioItemListCreateView(generics.ListCreateAPIView):
    serializer_class = PortfolioItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PortfolioItem.objects.filter(portfolio__user=user)

    def perform_create(self, serializer):
        serializer.save()

class PortfolioItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PortfolioItem.objects.all()
    serializer_class = PortfolioItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(portfolio__user=self.request.user)




import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


from rest_framework.views import APIView
from rest_framework.response import Response

class PortfolioMetricsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        portfolio_items = PortfolioItem.objects.filter(portfolio__user=user)
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")

        # Fetch historical stock data
        stock_data = {}
        for item in portfolio_items:
            stock = item.stock
            stock_info = yf.download(stock.symbol, start=start_date, end=end_date)
            stock_data[stock.symbol] = stock_info

        # Calculate metrics
        portfolio_value = self.calculate_portfolio_value(portfolio_items, stock_data)

        metrics = {
            "portfolio_value": portfolio_value,
            "portfolio_value_at_purchase": self.calculate_portfolio_value_at_purchase(portfolio_items),
            "pnl": self.calculate_pnl(portfolio_items, stock_data),
            "beta": self.calculate_beta(portfolio_items, stock_data, start_date, end_date),
            # Add other metrics here
        }

        return Response(metrics)

    def calculate_pnl(self, portfolio_items, stock_data):
        pnl = 0
        for item in portfolio_items:
            stock = item.stock
            current_price = stock_data[stock.symbol]["Close"].iloc[-1]
            profit = (current_price - float(item.purchase_price)) * item.shares
            pnl += profit
        return pnl

    def calculate_beta(self, portfolio_items, stock_data, start_date, end_date):
        market_index_symbol = "^GSPC"  # S&P 500
        market_index_data = yf.download(market_index_symbol, start=start_date, end=end_date)
        market_returns = market_index_data["Close"].pct_change().dropna()

        portfolio_beta = 0
        for item in portfolio_items:
            stock = item.stock
            stock_returns = stock_data[stock.symbol]["Close"].pct_change().dropna()
            covariance = stock_returns.cov(market_returns)
            market_variance = market_returns.var()
            beta = covariance / market_variance

            # Calculate the weight of the stock in the portfolio
            stock_weight = (item.shares * float(item.purchase_price)) / self.calculate_portfolio_value(portfolio_items, stock_data)

            # Calculate the weighted beta
            weighted_beta = stock_weight * beta
            portfolio_beta += weighted_beta

        return portfolio_beta

    def calculate_portfolio_value(self, portfolio_items, stock_data):
        portfolio_value = 0
        for item in portfolio_items:
            stock = item.stock
            current_price = stock_data[stock.symbol]["Close"].iloc[-1]
            value = current_price * item.shares
            portfolio_value += value
        return portfolio_value

    def calculate_portfolio_value_at_purchase(self, portfolio_items):
        portfolio_value_at_purchase = 0
        for item in portfolio_items:
            value_at_purchase = item.shares * float(item.purchase_price)
            portfolio_value_at_purchase += value_at_purchase
        return portfolio_value_at_purchase



from django.utils import timezone


class PortfolioValueOverTimeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        portfolio_items = PortfolioItem.objects.filter(portfolio__user=user)

        # Determine the date of the first transaction and set the start_date 7 days earlier
        first_transaction_date = portfolio_items.order_by("transaction_date").first().transaction_date.date()
        start_date = (first_transaction_date - timedelta(days=7)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")

        # Fetch historical stock data with an hourly interval
        stock_data = {}
        for item in portfolio_items:
            stock = item.stock
            stock_info = yf.download(stock.symbol, start=start_date, end=end_date, interval="1d")
            stock_info = stock_info.fillna(method='ffill')  # Fill missing values with the most recent available price
            stock_data[stock.symbol] = stock_info

        # Calculate the portfolio value over time
        portfolio_value_over_time = self.calculate_portfolio_value_over_time(portfolio_items, stock_data, start_date, end_date)

        return Response(portfolio_value_over_time)

    def calculate_portfolio_value_over_time(self, portfolio_items, stock_data, start_date, end_date):
        date_range = pd.date_range(start=start_date, end=end_date, freq="D")
        portfolio_value_over_time = {}

        for date in date_range:
            date = timezone.make_aware(date)
            portfolio_value = 0
            for item in portfolio_items:
                if item.transaction_date <= date:
                    stock = item.stock
                    stock_info = stock_data[stock.symbol]
                    if not stock_info.empty:
                        current_price = stock_info.loc[stock_info.index <= date, "Close"].iloc[-1]
                        value = current_price * item.shares
                        portfolio_value += value

            portfolio_value_over_time[date.strftime("%Y-%m-%d %H:%M:%S")] = portfolio_value

        return portfolio_value_over_time




