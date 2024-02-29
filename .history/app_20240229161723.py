from flask import Flask, redirect, render_template, request, url_for
from document_preprocessor import *
from indexing import *
from ranker import *
import pandas as pd
from image2text import *
from doinstruct_pix2pix import *

app = Flask(__name__)
UPLOAD_FOLDER = "tmp"
app.config["TMP_FOLDER"] = UPLOAD_FOLDER


def initialize_all():
    MAIN_INDEX_STEMMED = "Index_stemmed"
    STOPWORD_PATH = "data/stopwords.txt"

    # stopwords
    stopwords = set()
    with open(STOPWORD_PATH, "r", encoding="utf-8") as file:
        for stopword in file:
            stopwords.add(stopword.strip())

    # index
    main_index = BasicInvertedIndex()
    main_index.load(MAIN_INDEX_STEMMED)

    # processor
    preprocessor = RegexTokenizer(token_regex=r"[\w\.-]+", stemming=True)

    bm25 = BM25(main_index)
    pipeline = Ranker(main_index, preprocessor, stopwords, bm25)
    return pipeline


def get_results_all(ranker, query, top_n, args=None):
    DATASET_CSV_PATH = "data/data.csv.zip"
    results = ranker.query(query)
    docids = [result[0] for result in results]
    df = pd.read_csv(DATASET_CSV_PATH)
    if args is None:
        df_results = df.iloc[docids]
    else:
        df_results = df.iloc[docids]
        for arg in args:
            if arg:
                arg = arg.split(",")
                prompt_filter = ""
                for tag in arg:
                    prompt_filter += (
                        r'df_results["prompt"].str.contains(fr"\b'
                        + tag
                        + r'\b", regex=True, case=False) | '
                    )
                df_results = df_results[eval(prompt_filter[:-3])]
    prompts = df_results["prompt"].tolist()[:top_n]
    urls = df_results["pic_url"].tolist()[:top_n]
    return prompts, urls


engine = initialize_all()


@app.route("/")
def home():
    query = "A mountain in spring"
    print(query)
    prompts, urls = get_results_all(engine, query, 200)
    result = list(zip(prompts, urls))
    return render_template("index.html", result=result)


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        query = request.form.get("query")
        if not query:
            query = "A mountain in spring with white cloud"
        style = request.form.get("style")
        scene = request.form.get("scene")
        medium = request.form.get("medium")
        light = request.form.get("light")
        quality = request.form.get("quality")
        print(query)
        print(style)
        print(scene)
        print(medium)
        print(light)
        print(quality)
        args = [style, scene, medium, light, quality]
        prompts, urls = get_results_all(engine, query, 200, args)
        result = list(zip(prompts, urls))
        return render_template(
            "search.html",
            result=result,
            query=query,
            style=style,
            scene=scene,
            medium=medium,
            light=light,
            quality=quality,
        )
    return redirect(url_for("home"))


@app.route("/search_picture", methods=["POST", "GET"])
def search_picture():
    if request.method == "POST":
        query = request.files["img"]
        query = image2textData(query)
        if not query:
            query = "A mountain in spring with white cloud"
        style = request.form.get("style")
        scene = request.form.get("scene")
        medium = request.form.get("medium")
        light = request.form.get("light")
        quality = request.form.get("quality")
        print(query)
        print(style)
        print(scene)
        print(medium)
        print(light)
        print(quality)
        args = [style, scene, medium, light, quality]
        prompts, urls = get_results_all(engine, query, 200, args)
        result = list(zip(prompts, urls))
        return render_template(
            "search.html",
            result=result,
            query=query,
            style=style,
            scene=scene,
            medium=medium,
            light=light,
            quality=quality,
        )
    return redirect(url_for("home"))


@app.route("/submit_a_picture", methods=["POST", "GET"])
def submit_a_picture():
    if request.method == "POST":
        query = request.files["img"]
        text = image2textData(query)
        query.save("temp.jpeg")

        # ans=getResult("Add an eyeglass above the eye")
        # print(ans)
        # print(ans[0])
        return render_template("current_picture.html", currentValue=text, pic="0")
    return redirect(url_for("home"))


@app.route("/search_change", methods=["POST", "GET"])
def search_change():
    if request.method == "POST":
        query = request.form.get("willing_change")
        print(query)
        print(request.form)
        exit()
        result = getResult(query)
        # ans=getResult("Add an eyeglass above the eye")
        # print(ans)
        # print(ans[0])
        return render_template(
            "current_picture.html", currentValue=query, pic=result[0]
        )
    return redirect(url_for("home"))


if __name__ == "__main__":
    # engine = initialize_all()
    app.run(debug=True)
