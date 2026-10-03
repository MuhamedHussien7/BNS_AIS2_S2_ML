import os
import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
import pandas as pd
from sklearn.metrics import make_scorer, r2_score
from sklearn.model_selection import GridSearchCV, ShuffleSplit, train_test_split
from sklearn.tree import DecisionTreeRegressor

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "housing.csv")


# ---------------------------- model (same as notebook) ----------------------------
def fit_model(X, y):
    cv_sets = ShuffleSplit(n_splits=10, test_size=0.20, random_state=0)
    grid = GridSearchCV(
        DecisionTreeRegressor(random_state=0),
        {"max_depth": list(range(1, 11))},
        scoring=make_scorer(r2_score),
        cv=cv_sets,
    )
    return grid.fit(X, y).best_estimator_


def load_and_train(path=CSV_PATH):
    data = pd.read_csv(path)
    prices = data["MEDV"]
    features = data.drop("MEDV", axis=1)
    X_train, X_test, y_train, y_test = train_test_split(
        features, prices, test_size=0.2, random_state=1
    )
    model = fit_model(X_train, y_train)
    info = {
        "columns": list(features.columns),
        "depth": model.get_params()["max_depth"],
        "r2": r2_score(y_test, model.predict(X_test)),
        "min": prices.min(), "max": prices.max(),
        "mean": prices.mean(), "median": prices.median(),
        "ranges": {c: (features[c].min(), features[c].max()) for c in features.columns},
    }
    return model, info


# ---------------------------------- GUI ----------------------------------
class App(tk.Tk):
    FIELDS = [
        ("RM", "Average number of rooms (RM)"),
        ("LSTAT", "Lower-class workers % (LSTAT)"),
        ("PTRATIO", "Student-teacher ratio (PTRATIO)"),
    ]

    def __init__(self, model, info):
        super().__init__()
        self.model, self.info = model, info
        self.title("Boston Housing Price Predictor")
        self.resizable(False, False)
        self.entries = {}
        self._build()

    def _build(self):
        pad = {"padx": 12, "pady": 6}
        ttk.Label(self, text="Boston Housing Price Predictor",
                  font=("Segoe UI", 15, "bold")).grid(row=0, column=0, columnspan=3, pady=(14, 2))
        ttk.Label(self, text=f"Decision Tree (max_depth = {self.info['depth']})  |  "
                             f"Test R² = {self.info['r2']:.3f}",
                  foreground="#555").grid(row=1, column=0, columnspan=3, pady=(0, 8))

        for r, (key, label) in enumerate(self.FIELDS, start=2):
            lo, hi = self.info["ranges"][key]
            ttk.Label(self, text=label).grid(row=r, column=0, sticky="w", **pad)
            e = ttk.Entry(self, width=12, justify="center")
            e.grid(row=r, column=1, **pad)
            e.bind("<Return>", lambda _e: self.predict())
            self.entries[key] = e
            ttk.Label(self, text=f"({lo:g} - {hi:g})", foreground="#888").grid(row=r, column=2, sticky="w", padx=(0, 12))

        btns = ttk.Frame(self)
        btns.grid(row=5, column=0, columnspan=3, pady=10)
        ttk.Button(btns, text="Predict Price", command=self.predict).pack(side="left", padx=6)
        ttk.Button(btns, text="Clear", command=self.clear).pack(side="left", padx=6)

        self.result = tk.StringVar(value="Enter the values and press Predict")
        ttk.Label(self, textvariable=self.result, font=("Segoe UI", 14, "bold"),
                  foreground="#1a6b2f").grid(row=6, column=0, columnspan=3, pady=(4, 2))
        self.compare = tk.StringVar()
        ttk.Label(self, textvariable=self.compare, foreground="#444").grid(
            row=7, column=0, columnspan=3, pady=(0, 14))

    def predict(self):
        values = []
        for key, label in self.FIELDS:
            txt = self.entries[key].get().strip()
            try:
                v = float(txt)
            except ValueError:
                messagebox.showerror("Invalid input", f"'{label}' must be a number.")
                return
            lo, hi = self.info["ranges"][key]
            if not (lo <= v <= hi):
                if not messagebox.askyesno(
                        "Out of range",
                        f"{key} = {v:g} is outside the data range ({lo:g} - {hi:g}).\n"
                        "The prediction may be unreliable. Continue?"):
                    return
            values.append(v)

        x = pd.DataFrame([values], columns=self.info["columns"])
        price = float(self.model.predict(x)[0])
        self.result.set(f"Predicted price: ${price:,.2f}")
        diff = price - self.info["median"]
        side = "above" if diff >= 0 else "below"
        self.compare.set(f"${abs(diff):,.0f} {side} the dataset median (${self.info['median']:,.0f})")

    def clear(self):
        for e in self.entries.values():
            e.delete(0, tk.END)
        self.result.set("Enter the values and press Predict")
        self.compare.set("")


if __name__ == "__main__":
    if not os.path.exists(CSV_PATH):
        raise SystemExit(f"housing.csv not found next to this script: {CSV_PATH}")
    model, info = load_and_train()
    App(model, info).mainloop()