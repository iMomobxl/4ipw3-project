

const imageNotFound = (image) => {
    image.onerror = null;
    image.src = "/static/app/media/default.jpeg";
}