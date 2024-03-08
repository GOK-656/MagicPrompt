from flask import Flask, redirect, render_template, request, url_for
from document_preprocessor import *
from indexing import *
from ranker import *
import pandas as pd
from image2text import *
from doinstruct_pix2pix import *
import tempfile
from prompt_generator import *
from load_drawingModels import *
import uuid

app = Flask(__name__)
app.config["TEMP_FOLDER"] = "tmp/"


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
    DATASET_CSV_PATH = "data/data_with_labels.csv.zip"
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
    query = "A mountain in spring with white cloud"
    print(query)
    prompts, urls = get_results_all(engine, query, 200)
    result = list(zip(prompts, urls))
    return render_template("index.html", result=result, query=query)


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST" or request.method == "GET":
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
        # with tempfile.NamedTemporaryFile() as temp_file:
        #     query.save(temp_file.name)
        #     temp_file_path = temp_file.name
        #     print(temp_file_path)
        #     img2url(open(temp_file_path, "rb"))
        img = Image.open(query)
        if not os.path.exists("tmp"):
            os.makedirs("tmp")
        save_path = os.path.join("tmp", query.filename)
        # save_path = "tmp/" + "tmp." + query.filename.split(".")[-1]
        print("save path: ", save_path)
        img.save(save_path)
        img_stream = ""
        img_stream = base64.b64encode(open(save_path, "rb").read()).decode("utf-8")
        # with open(save_path, "rb") as img_file:
        # img_stream = base64.b64encode(img_file.read()).decode("utf-8")
        # ans=getResult("Add an eyeglass above the eye")
        # print(ans)
        # print(ans[0])
        # img_stream = get_pix2pix_result("add a bird to sky", save_path)
        os.remove(save_path)
        return render_template(
            "current_picture.html", currentValue=text, pic="0", img_stream=img_stream
        )
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


@app.route("/reset", methods=["POST"])
def reset():
    query = "A mountain in spring with white cloud"
    return render_template("generate.html", query=query, flag=True)


@app.route("/pix2pix", methods=["POST"])
def pix2pix():
    if request.method == "POST":
        query = request.form.get("query")
        model = request.form.get("model")
        if not query:
            query = "A mountain in spring with white cloud"
        generated_text = request.form.get("generated_text")
        img_stream = request.form.get("img_stream")
        flag = request.form.get("flag")
        inputprompt = request.form.get("inputprompt")
        steps = request.form.get("steps")
        text_cfg = request.form.get("text_cfg")
        img_cfg = request.form.get("image_cfg")
        img_bytes = base64.b64decode(img_stream)
        file_name = str(uuid.uuid4()) + ".jpg"
        img = Image.open(io.BytesIO(img_bytes))
        img.save(os.path.join("tmp", file_name))

        if not steps:
            steps = 10
        if not text_cfg:
            text_cfg = 7.5
        if not img_cfg:
            img_cfg = 1.5
        print(steps, text_cfg, img_cfg)
        if not inputprompt:
            inputprompt = "add a bird to the sky"

        print("file_name", file_name)
        modified_img, flag_pix2pix = get_pix2pix_result(
            inputprompt, os.path.join("tmp", file_name), steps, text_cfg, img_cfg
        )

        # flag_pix2pix = False
        return render_template(
            "generate.html",
            query=query,
            model=model,
            generated_text=generated_text,
            img_stream=img_stream,
            flag=flag,
            modified_img=modified_img,
            flag_pix2pix=flag_pix2pix,
            # file_name=file_name,
        )


@app.route("/generate", methods=["POST", "GET"])
def generate():
    if request.method == "POST":
        print(request.form)
        query = request.form.get("query")
        model = request.form.get("model")
        if not query:
            query = "A mountain in spring with white cloud"
        generated_text = prompt_generator(query)
        print(generated_text)
        print("selected model", model)
        flag = True

        img_bytes = None
        if model == "stable_diffusion":
            img_bytes, flag = diffusion_image(generated_text)
        elif model == "lora":
            img_bytes, flag = lora_image(generated_text)
        elif model == "lexica":
            img_bytes, flag = midjourney_image(generated_text)
        elif model == "midjourney":
            img_bytes, flag = lexica_image(generated_text)
        else:
            img_bytes, flag = diffusion_image(generated_text)

        # print(img_stream)
        print(flag)
        img_stream = ""
        if img_bytes:
            # file_name = str(uuid.uuid4()) + ".jpg"
            # image = Image.open(io.BytesIO(img_bytes))
            # image.save(os.path.join("tmp", file_name))
            img_stream = base64.b64encode(img_bytes).decode("utf-8")
        return render_template(
            "generate.html",
            query=query,
            model=model,
            generated_text=generated_text,
            img_stream=img_stream,
            flag=flag,
            flag_pix2pix=True,
            # file_name=file_name,
        )
    elif request.method == "GET":
        query = "A mountain in spring with white cloud"
        return render_template(
            "generate.html", query=query, flag=True, flag_pix2pix=True
        )

    return redirect(url_for("home"))


if __name__ == "__main__":
    # engine = initialize_all()
    app.run(debug=True)
