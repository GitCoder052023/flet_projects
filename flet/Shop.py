import pyrebase as base
from flet import *
import flet as ft
from functools import partial
from Dev.Managers import User_manager

# SETTING UP FIREBASE and MongoDB CONFIGS
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

manager = User_manager.DB_manager("mongodb://localhost:27017/", "Orders", "orders")


# Creating Order form

def order_form(page: ft.Page):
    page.route = "/OrderForm"
    page.title = "Simple store"
    page.bgcolor = "#ffffff"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    def submit_order(e):
        product = product_name_field.value
        name = name_field.value
        phone = phone_field.value
        address = address_field.value
        payment_method = payment_radio_group.value

        if product and name and phone and address and payment_method is not None:
            product_data = {
                "Product": product,
                "Name": name,
                "Phone": phone,
                "Address": address,
                "Payment Method": payment_method
            }

            manager.create(product_data)

            dlg = ft.AlertDialog(
                title=Text("Order placed successfully!"),
                content=Text("Thank you for ordering product from our app, your order will arrive soon!"),
                on_dismiss=lambda e: page.go("/products"),
            )

            page.dialog = dlg
            dlg.open = True
            page.update()

        else:
            dlg = ft.AlertDialog(
                title=Text("Please fill out all fields!")
            )
            page.dialog = dlg
            dlg.open = True
            page.update()

    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        icon_size=30,
        on_click=lambda e: page.go("/products"),  # Change the route to the desired page
    )

    product_name_field = ft.TextField(
        height=48,
        width=255,
        bgcolor="#f0f3f6",
        text_size=12,
        color="black",
        border_color="transparent",
        hint_text="Product name",
        filled=True,
        cursor_color="black",
        hint_style=ft.TextStyle(
            size=11,
            color="black",
        ),
    )

    name_field = ft.TextField(
        height=48,
        width=255,
        bgcolor="#f0f3f6",
        text_size=12,
        color="black",
        border_color="transparent",
        hint_text="Name",
        filled=True,
        cursor_color="black",
        hint_style=ft.TextStyle(
            size=11,
            color="black",
        ),
    )

    phone_field = ft.TextField(
        height=48,
        width=255,
        bgcolor="#f0f3f6",
        text_size=12,
        color="black",
        border_color="transparent",
        hint_text="Phone Number",
        filled=True,
        cursor_color="black",
        hint_style=ft.TextStyle(
            size=11,
            color="black",
        ),
    )

    address_field = ft.TextField(
        height=48,
        width=255,
        bgcolor="#f0f3f6",
        text_size=12,
        color="black",
        border_color="transparent",
        hint_text="Address",
        filled=True,
        cursor_color="black",
        hint_style=ft.TextStyle(
            size=11,
            color="black",
        ),
    )

    cod_radio = ft.Radio(value="COD", label="COD")
    online_radio = ft.Radio(value="Online", label="Online")
    payment_radio_group = ft.RadioGroup(content=ft.Row(
        controls=[cod_radio, online_radio],
        spacing=10,
    ))

    submit_button = ft.ElevatedButton(
        on_click=submit_order,
        content=ft.Text(
            "Submit Order",
            size=11,
            weight="bold",
        ),
        style=ft.ButtonStyle(
            shape={"": ft.RoundedRectangleBorder(radius=8)},
            color={"": "white"}
        ),
        height=48,
        width=255,
    )

    order_form_container = ft.Container(
        width=280,
        height=600,
        bgcolor="#ffffff",  # changed bgcolor to white
        padding=12,
        border_radius=35,  # added border radius
        border=border.all(2, "Transparent"),
        alignment=alignment.center,
        content=ft.Container(
            content=ft.Column(
                spacing=20,
                horizontal_alignment="center",
                controls=[
                    ft.Text(
                        "Order Product",
                        size=15,
                        text_align="center",
                        weight="bold",
                        color="black"
                    ),
                    product_name_field,
                    name_field,
                    phone_field,
                    address_field,
                    ft.Text(
                        "Payment Method",
                        size=12,
                        color="black",
                    ),
                    payment_radio_group,
                    submit_button,
                    back_button
                ],
            ),
        )
    )

    # Add a new container here
    outer_container = ft.Container(
        content=order_form_container,
        padding=20,
        border_radius=35,
        bgcolor="#f0f3f6",
        alignment=ft.alignment.center,  # add this line
        expand=True
    )

    # Add a new container to center the outer_container
    centered_container = ft.Container(
        content=outer_container,
        padding=20,
        border_radius=35,
        bgcolor="#f0f3f6",
        alignment=ft.alignment.center,
    )

    return centered_container


# Define a landing page class ...
class Landing(ft.View):
    def __init__(self, page: ft.Page):
        super(Landing, self).__init__(
            route="/", horizontal_alignment="center", vertical_alignment="center"
        )

        self.page = page

        self.cart_logo = ft.Icon(name="shopping_cart_outlined", size=64)
        self.title = ft.Text("SIMPLE STORE".upper(), size=28, weight="bold")
        self.subtitle = ft.Text("Made With Flet", size=11)

        self.product_page_btn = ft.IconButton(
            "arrow_forward",
            width=54,
            height=54,
            style=ft.ButtonStyle(
                bgcolor={"": "#202020"},
                shape={"": ft.RoundedRectangleBorder(radius=8)},
                side={"": ft.BorderSide(2, "white54")},
            ),
            on_click=lambda e: self.page.go("/products"),
        )

        self.controls = [
            self.cart_logo,
            ft.Divider(height=25, color="transparent"),
            self.title,
            self.subtitle,
            ft.Divider(height=10, color="transparent"),
            self.product_page_btn,
        ]


# Define your model class => class that stores your data
class Model(object):
    products: dict = {
        0: {
            "id": "111",
            "img_src": "assets/phone1.jpg",
            "name": "Product 1",
            "description": "Experience the excellence of Product 1, a cutting-edge creation designed to elevate your daily routine. Crafted with precision and innovation, this product offers unmatched quality and performance. Enhance your lifestyle with Product 1 today.",
            "price": "$21.55",
        },
        1: {
            "id": "222",
            "img_src": "assets/phone2.jpg",
            "name": "Product 2",
            "description": "Immerse yourself in the sophistication of Product 2. Uniquely crafted to meet your needs, this product combines style and functionality seamlessly. Elevate your daily experiences with the exceptional features of Product 2.",
            "price": "$32.99",
        },
        2: {
            "id": "333",
            "img_src": "assets/phone3.jpg",
            "name": "Product 3",
            "description": "Discover the versatility of Product 3, a dynamic solution designed for modern living. Whether it's convenience, durability, or style you seek, Product 3 delivers on all fronts. Make a statement with this exceptional product",
            "price": "$45.75",
        },
    }

    cart: dict = {}

    @staticmethod
    def get_products():
        return Model.products

    @staticmethod
    def get_cart():
        return Model.cart

    @staticmethod
    def add_item_to_cart(data: str):
        for _, values in Model.products.items():
            for key, value in values.items():
                if value == data:
                    if not Model.cart.get(value):
                        Model.cart[value] = {"quantity": 1, **values}

                    else:
                        Model.cart[value]["quantity"] += 1


# Next, define the product page ...
class Product(ft.View):
    def __init__(self, page: ft.Page):
        super(Product, self).__init__(route="/products")
        self.page = page
        self.initilize()

    # we break the UI compoenents into several functions for better code readability

    # a method to initilize everythong
    def initilize(self):
        # this is the main row where items apepar ,,,
        self.products = ft.Row(expand=True, scroll="auto", spacing=30)
        self.create_products()

        self.controls = [
            self.display_product_page_header(),
            ft.Text("Shop", size=32),
            ft.Text("Select items from the list below"),
            self.products,
            self.display_product_page_footer(),
        ]

    def display_product_page_footer(self):
        return ft.Row([ft.Text("Simple X Shop", size=10)], alignment="center")

    def display_product_page_header(self):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon("settings", size=18),
                    ft.IconButton(
                        "shopping_cart_outlined",
                        on_click=lambda e: self.page.go("/cart"),
                        icon_size=18,
                    ),
                ],
                alignment="spaceBetween",
            )
        )

    # Define a method that creates the product UI items from the Model
    def create_products(self, products: dict = Model.get_products()):
        # loop over the data and extract the info based on keys
        for _, values in products.items():
            for (
                    key,
                    value,
            ) in values.items():
                # values.items() has a specific key:value pairing system
                if key == "img_src":
                    img_src = self.create_product_image(img_path=value)
                elif key == "name":
                    name = values["name"]
                elif key == "description":
                    description = values["description"]
                elif key == "id":
                    idd = values["id"]
                elif key == "price":
                    price = self.create_product_event(values["price"], idd)

            texts = self.create_product_text(name, description)

            self.create_full_item_view(img_src, texts, price)

    # define a gather method that compiles everything
    def create_full_item_view(self, img_src, texts, price):
        item = ft.Column()

        item.controls.append(self.create_product_container(4, img_src))
        item.controls.append(self.create_product_container(4, texts))
        item.controls.append(self.create_product_container(1, price))

        self.products.controls.append(self.create_item_wrapper(item))

    # a final wraper method
    def create_item_wrapper(self, item: ft.Column):
        return ft.Container(
            width=250, height=450, content=item, padding=8, border_radius=6
        )

    # define am ethod for the image UI
    def create_product_image(self, img_path: str):
        return ft.Container(
            image_src=img_path, image_fit="fill", border_radius=6, padding=10
        )

    # define a method for the text UI (name + description)
    def create_product_text(self, name: str, description: str):
        return ft.Column([ft.Text(name, size=18), ft.Text(description, size=11)])

    # define a method for prie and a add_to_cart button
    def create_product_event(self, price: str, idd: str):
        # we use the idd to keep track of the products being clicked
        return ft.Row(
            [
                ft.Text(price, size=14),
                ft.IconButton(
                    "add",
                    data=idd,
                    on_click=self.add_to_cart,
                ),
                ft.IconButton(
                    icon=icons.SHOPPING_CART,
                    on_click=lambda _: self.page.go("/OrderForm")
                )
            ],
            alignment="spaceBetween",
        )

    # A method to wrap our product card inside a container
    def create_product_container(self, expand: bool, control: ft.control):
        return ft.Container(content=control, expand=expand, padding=5)

    # before the cart, one final method to add items to the cart
    def add_to_cart(self, e: ft.TapEvent):
        Model.add_item_to_cart(data=e.control.data)
        print(Model.cart)


# Finally, we define our cart class
class Cart(ft.View):
    def __init__(self, page: ft.Page):
        super(Cart, self).__init__(route="/cart")
        self.page = page
        self.initilize()

    # similiar to the products page, we break down the UI cart into functions

    # a method to initilize
    def initilize(self):
        self.cart_items = ft.Column(spacing=20)
        self.create_cart()

        self.controls = [
            ft.Row(
                [
                    ft.IconButton(
                        "arrow_back_ios_new_outlined",
                        on_click=lambda e: self.page.go("/products"),
                        icon_size=16,
                    )
                ],
                alignment="spaceBetween",
            ),
            ft.Text("Cart", size=32),
            ft.Text("Your cart items"),
            self.cart_items,
        ]

    def create_cart(self, cart: dict = Model.get_cart()):
        for _, values in cart.items():
            for key, value in values.items():
                if key == "img_src":
                    img_src = self.create_item_image(img_path=value)
                elif key == "quantity":
                    quantity = self.create_item_quantity(values["quantity"])
                elif key == "name":
                    name = self.create_item_name(values["name"])
                elif key == "price":
                    price = self.create_item_price(values["price"])

            self.compile_cart_item(img_src, quantity, name, price)

    # we also have a method to compile all the items
    def create_cart_item(self):
        return ft.Row(alignment="spaceBetween")

    def compile_cart_item(self, img_src, quantity, name, price):
        row = self.create_cart_item()

        row.controls.append(img_src)
        row.controls.append(name)
        row.controls.append(quantity)
        row.controls.append(price)

        self.cart_items.controls.append(self.create_item_wrap(row))

    # we can now create the seperate UI components for each data
    def create_item_wrap(self, control: ft.Control):
        return ft.Container(
            content=control,
            padding=10,
            border=ft.border.all(1, "white10"),
            border_radius=6,
        )

    def create_item_image(self, img_path):
        return ft.Container(width=32, height=32, image_src=img_path, bgcolor="teal")

    def create_item_quantity(self, quantity: int):
        return ft.Text(f"{quantity} X")

    def create_item_name(self, name: str):
        return ft.Text(name, size=16)

    def create_item_price(self, price: str):
        return ft.Text(price)


# DESIGNING FORM UI
class UserWidget(UserControl):
    def __init__(self, title: str, sub_title: str, btn_name: str, func):
        self._title = title
        self._sub_title = sub_title
        self._btn_name = btn_name
        self._func = func
        super().__init__()

    def InputTextField(self, text: str, hide: bool, CRP: bool):
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
                password=hide,
                can_reveal_password=CRP

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

    def _create_switch_text_button(self, question: str, link_text: str, func):
        return Row(
            controls=[
                Text(
                    question,
                    color="black",
                    size=12,
                ),
                TextButton(
                    text=link_text,
                    on_click=func,
                ),
            ],
            alignment="center",
        )

    def build(self):
        title_container = Container(
            alignment=alignment.center,
            content=Text(
                self._title,
                size=15,
                text_align="center",
                weight="bold",
                color="black"
            )
        )

        subtitle_container = Container(
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

        self._switch_text_button = self._create_switch_text_button("", func=partial(self._func), link_text="")

        return Column(
            horizontal_alignment="center",
            controls=[
                Container(padding=10),
                title_container,  # add the title container
                subtitle_container,  # add the subtitle container

                Column(
                    spacing=12,
                    controls=[
                        self.InputTextField("Email", False, False),
                        self.InputTextField("Password", True, True)
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
                ),
                self._switch_text_button,
            ]
        )


def main(page: Page):
    # SETTING UP PAGE CONFIGS
    page.title = "Simple store"
    page.bgcolor = "#f0f3f6"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    def router(route):
        page.views.clear()

        if page.route == "/":
            landing = Landing(page)
            page.views.append(landing)

        if page.route == "/products":
            products = Product(page)
            page.views.append(products)

        if page.route == "/cart":
            cart = Cart(page)
            page.views.append(cart)

        if page.route == "/OrderForm":  # Add this line
            page.views.append(order_form(page))  # Add the order_form view

        page.update()

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
            dlg = ft.AlertDialog(
                title=Text("Registration successful!"),
            )

            page.dialog = dlg
            dlg.open = True
            page.update()
        except Exception as ex:
            print(ex)

    def validate_user(e):
        try:
            base_auth.sign_in_with_email_and_password(
                _sign_in_.controls[0].controls[3].controls[0].content.value,
                _sign_in_.controls[0].controls[3].controls[1].content.value,
            )

            page.views.clear()
            page.on_route_change = router
            page.go("/")
        except:
            dlg = ft.AlertDialog(
                title=Text("Wrong credentials!")
            )

            page.dialog = dlg
            dlg.open = True
            page.update()

    def show_login_form(e):
        _sign_in_main.content.controls[1] = _sign_in_
        _sign_in_main.content.controls[2] = _sign_in_._create_switch_text_button("Don't have an account? ",
                                                                                 "Register here", show_register_form)
        page.update()

    def show_register_form(e):
        _sign_in_main.content.controls[1] = _register_
        _sign_in_main.content.controls[2] = _register_._create_switch_text_button("Already have an account? ",
                                                                                  "Login here", show_login_form)
        page.update()

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
    _sign_in_main.content.controls.append(
        _sign_in_._create_switch_text_button("Don't have an account?", func=show_register_form,
                                             link_text="Register here"))

    page.add(_sign_in_main)

    show_login_form(None)


if __name__ == "__main__":
    flet.app(target=main)