from mvc_flask import Router


Router.get("/", "home#index")

Router.get("/login", "auth#login")
Router.put("/login", "auth#login")

Router.get("/register", "auth#register")
Router.put("/register", "auth#register")

Router.get("/logout", "auth#logout")
Router.put("/logout", "auth#logout")

Router.get("/delete", "auth#delete")
Router.delete("/delete", "auth#delete")

Router.get("/update", "blog#update")
Router.put("/update", "blog#update")

Router.get("/user", "blog#user")

Router.get("/admin", "admin#admin")
Router.put("/admin", "admin#admin")