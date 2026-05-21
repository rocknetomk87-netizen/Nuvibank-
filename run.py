from core_bank.core_app import create_app

app = create_app()

if __name__ == "__main__":
    print("NUVIBANK CORE ONLINE")
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )
