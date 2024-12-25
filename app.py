from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Dataset Paths
dataset_path = 'dataset.csv'
graph_dir = 'static/graphs'

# Load dataset globally
original_data = pd.read_csv(dataset_path)
data = original_data.copy()

# Ensure graph directory exists
os.makedirs(graph_dir, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


def save_graph(fig, filename):
    path = os.path.join(graph_dir, filename)
    fig.savefig(path)
    plt.close(fig)
    return path


@app.route('/get_data', methods=['GET'])
def get_data():
    global data
    try:
        data_preview = data.head(10).to_dict(orient='records')
        total_rows = len(data)
        return jsonify({"data": data_preview, "total_rows": total_rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/general_info', methods=['GET'])
def general_info():
    global data
    try:
        info = {
            "columns": list(data.columns),
            "dtypes": data.dtypes.astype(str).to_dict(),
            "total_rows": len(data),
            "total_columns": len(data.columns)
        }
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/missing_data', methods=['GET'])
def missing_data():
    global data
    try:
        missing = data.isnull().sum()

        fig, ax = plt.subplots()
        missing.plot(kind='bar', color='orange', ax=ax)
        ax.set_title('Missing Data per Column')
        ax.set_xlabel('Columns')
        ax.set_ylabel('Missing Count')
        graph_path = save_graph(fig, 'missing_data.png')

        return jsonify({
            "missing_counts": missing.to_dict(),
            "graph": graph_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/popular_products', methods=['GET'])
def popular_products():
    global data
    try:
        if 'Product' not in data.columns:
            return jsonify({"error": "'Product' column not found in dataset."})

        product_counts = data['Product'].dropna().value_counts().head(10)

        # Convert index and values to regular Python types
        product_counts_dict = product_counts.to_dict()
        product_counts_dict = {str(k): int(v) for k, v in product_counts_dict.items()}

        fig, ax = plt.subplots()
        product_counts.plot(kind='bar', color='skyblue', ax=ax)
        ax.set_title('Top 10 Popular Products')
        ax.set_xlabel('Products')
        ax.set_ylabel('Count')
        graph_path = save_graph(fig, 'popular_products.png')

        return jsonify({
            "most_popular_product": product_counts.idxmax(),
            "count": int(product_counts.max()),
            "total_unique_products": int(data['Product'].nunique()),
            "graph": graph_path,
            "product_counts": product_counts_dict
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/city_sales', methods=['GET'])
def city_sales():
    global data
    try:
        city_sales = data.groupby('City')['Total_Cost'].sum().sort_values(ascending=False).head(10)

        fig, ax = plt.subplots()
        city_sales.plot(kind='bar', color='green', ax=ax)
        ax.set_title('Top 10 Cities by Sales')
        ax.set_xlabel('City')
        ax.set_ylabel('Total Sales')
        graph_path = save_graph(fig, 'city_sales.png')

        return jsonify({
            "top_cities": city_sales.to_dict(),
            "graph": graph_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/payment_distribution', methods=['GET'])
def payment_distribution():
    global data
    try:
        payment_counts = data['Payment_Method'].value_counts()

        fig, ax = plt.subplots()
        payment_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_title('Payment Method Distribution')
        graph_path = save_graph(fig, 'payment_distribution.png')

        return jsonify({
            "payment_methods": payment_counts.to_dict(),
            "graph": graph_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/discount_analysis', methods=['GET'])
def discount_analysis():
    global data
    try:
        discount_counts = data['Discount_Applied'].value_counts()

        fig, ax = plt.subplots()
        discount_counts.plot(kind='bar', color='purple', ax=ax)
        ax.set_title('Discount Analysis')
        ax.set_xlabel('Discount Applied')
        ax.set_ylabel('Count')
        graph_path = save_graph(fig, 'discount_analysis.png')

        return jsonify({
            "discount_counts": discount_counts.to_dict(),
            "graph": graph_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/customer_category_analysis', methods=['GET'])
def customer_category_analysis():
    global data
    try:
        category_sales = data.groupby('Customer_Category')['Total_Cost'].sum()

        fig, ax = plt.subplots()
        category_sales.plot(kind='bar', color='red', ax=ax)
        ax.set_title('Customer Category Sales')
        ax.set_xlabel('Customer Category')
        ax.set_ylabel('Total Sales')
        graph_path = save_graph(fig, 'customer_category_analysis.png')

        return jsonify({
            "category_sales": category_sales.to_dict(),
            "graph": graph_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/season_sales', methods=['GET'])
def season_sales():
    global data
    try:
        season_sales = data.groupby('Season')['Total_Cost'].sum()

        fig, ax = plt.subplots()
        season_sales.plot(kind='bar', color='gold', ax=ax)
        ax.set_title('Seasonal Sales')
        ax.set_xlabel('Season')
        ax.set_ylabel('Total Sales')
        graph_path = save_graph(fig, 'season_sales.png')

        return jsonify({
            "season_sales": season_sales.to_dict(),
            "graph": graph_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/promotion_analysis', methods=['GET'])
def promotion_analysis():
    global data
    try:
        promotion_counts = data['Promotion'].value_counts()

        fig, ax = plt.subplots()
        promotion_counts.plot(kind='bar', color='teal', ax=ax)
        ax.set_title('Promotion Analysis')
        ax.set_xlabel('Promotion')
        ax.set_ylabel('Count')
        graph_path = save_graph(fig, 'promotion_analysis.png')

        return jsonify({
            "promotion_counts": promotion_counts.to_dict(),
            "graph": graph_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route('/remove_missing', methods=['GET'])
def remove_missing():
    global data
    try:
        data = data.dropna()
        data_preview = data.head(10).to_dict(orient='records')
        total_rows = len(data)
        return jsonify({"data": data_preview, "total_rows": total_rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
