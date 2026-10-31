# shop

A tiny product catalogue over `sqlite3`. Run the tests with
`python3 -m unittest discover -s tests`.

Price tracking is off by default. Set `SHOP_TRACK_PRICES=1` to record each
price change the `set-price` route makes.
