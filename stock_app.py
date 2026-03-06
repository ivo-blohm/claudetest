from flask import Flask, jsonify, render_template
import yfinance as yf

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("stock.html")


@app.route("/api/tesla")
def tesla_data():
    ticker = yf.Ticker("TSLA")
    hist = ticker.history(period="6mo", interval="1d")
    hist = hist.reset_index()

    data = {
        "dates": hist["Date"].dt.strftime("%Y-%m-%d").tolist(),
        "open": hist["Open"].round(2).tolist(),
        "close": hist["Close"].round(2).tolist(),
        "high": hist["High"].round(2).tolist(),
        "low": hist["Low"].round(2).tolist(),
        "volume": hist["Volume"].tolist(),
    }

    info = ticker.fast_info
    data["current_price"] = round(float(info.last_price), 2)
    data["currency"] = info.currency

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
