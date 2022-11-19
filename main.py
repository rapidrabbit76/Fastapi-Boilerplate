import uvicorn


def main():
    app = "app.server:app"
    uvicorn.run(
        app,
        port=8080,
        host="0.0.0.0",
        workers=1,
        reload=True,
    )


if __name__ == "__main__":
    main()
