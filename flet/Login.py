import pyrebase as base
from flet import *
from functools import partial

# SETTING UP FIREBASE CONFIGS
base_configs = {"apiKey": "AIzaSyAYhUDEcVyHP_cwH1zgafkPw8hoqbWmBsQ",
                "authDomain": "m-fletlogin.firebaseapp.com",
                "projectId": "m-fletlogin",
                "storageBucket": "m-fletlogin.appspot.com",
                "messagingSenderId": "686739705989",
                "appId": "1:686739705989:web:39fc77702f2b41391e99ec",
                "measurementId": "G-RBKLB8QFZF",
                "databaseURL": ""}

app = base.initialize_app(base_configs)
base_auth = app.auth()

# DESIGNING FORM UI
class UserWidget(UserControl):
    def __init__(self, title: str, sub_title: str, btn_name: str, func):
        self._title = title
        self._sub_title = sub_title
        self._btn_name = btn_name
        self._func = func
        super().__init__()

    def InputTextField(self, text: str, hide: bool):
        return Container(
            alignment=alignment.center,
            content=TextField(
                height=48,
                width=255,
                bgcolor="#f0f3f6",
                text_size=12,
                color="black",
                border_color="transparent",
                hint_text=text,
                filled=True,
                cursor_color="black",
                hint_style=TextStyle(
                    size=11,
                    color="black",
                ),
                password=hide

            ),
        )

    def SigninOptions(self, path, name: str):
        return Container(
            ElevatedButton(
                content=Row(
                    alignment="center",
                    spacing=4,
                    controls=[
                        Image(src=path,
                              height=30,
                              width=30),
                        Text(
                            name,
                            color="black",
                            size=10,
                            weight="bold"
                        )
                    ]
                ),
                style=ButtonStyle(
                    shape={
                        "": RoundedRectangleBorder(radius=8)
                    },
                    bgcolor={
                        "": "#f0f3f6"
                    }
                )
            )
        )

    def build(self):
        self._title = Container(
            alignment=alignment.center,
            content=Text(
                self._title,
                size=15,
                text_align="center",
                weight="bold",
                color="black"

            )
        )

        self._sub_title = Container(
            alignment=alignment.center,
            content=Text(
                self._sub_title,
                size=10,
                text_align="center",
                weight="bold",
                color="black"

            )
        )

        self._sign_in_ = Container(
            content=ElevatedButton(on_click=partial(self._func),
                                   content=Text(
                                       self._btn_name,
                                       size=11,
                                       weight="bold",

                                   ),
                                   style=ButtonStyle(
                                       shape={"": RoundedRectangleBorder(radius=8)},
                                       color={"": "white"}
                                   ),
                                   height=48,
                                   width=255)
        )

        return Column(
            horizontal_alignment="center",
            controls=[
                Container(padding=10),
                self._title,
                self._sub_title,

                Column(
                    spacing=12,
                    controls=[
                        self.InputTextField("Email", False),
                        self.InputTextField("Password", True)
                    ]
                ),
                Container(padding=5),
                self._sign_in_,
                Container(padding=5),
                Column(
                    horizontal_alignment="center",
                    controls=[
                        Container(
                            content=Text(
                                "or continue with",
                                size=10,
                                color="black",
                            )
                        ),
                        self.SigninOptions("assets/google.png", "Google"),
                        self.SigninOptions("assets/facebook.png", "Facebook"),
                    ]
                )
            ]
        )


def main(page: Page):
    # SETTING UP PAGE CONFIGS
    page.title = "Login form"
    page.bgcolor = "#f0f3f6"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # SETTING UP PAGE UI
    def __main_column():
        return Container(
            width=280,
            height=600,
            bgcolor="#ffffff",
            padding=12,
            border_radius=35,
            content=Column(
                spacing=20,
                horizontal_alignment="center"
            )
        )

    def register_user(e):
        try:
            base_auth.create_user_with_email_and_password(
                _register_.controls[0].controls[3].controls[0].content.value,
                _register_.controls[0].controls[3].controls[1].content.value,
            )
            print("Registration Ok!")
        except Exception as ex:
            print(ex)

    def validate_user(e):
        try:
            base_auth.sign_in_with_email_and_password(
                _sign_in_.controls[0].controls[3].controls[0].content.value,
                _sign_in_.controls[0].controls[3].controls[1].content.value,
            )
            print("Login successful")
        except:
            print("Wrong credentials")

    _sign_in_ = UserWidget(
        "Welcome Back!",
        "Enter your account details below.",
        "Sign In",
        validate_user
    )

    _register_ = UserWidget(
        "Registration",
        "Register your email and password below.",
        "Register",
        register_user
    )

    _sign_in_main = __main_column()

    _sign_in_main.content.controls.append(Container(padding=15))
    _sign_in_main.content.controls.append(_sign_in_)

    _reg_main = __main_column()

    _reg_main.content.controls.append(Container(padding=15))
    _reg_main.content.controls.append(_register_)

    page.add(
        Row(
            alignment="center",
            spacing=25,
            controls=[
                _sign_in_main,
                _reg_main,
            ]
        )
    )


if __name__ == "__main__":
    flet.app(target=main, assets_dir="assets")