import tkinter as tk
from tkinter import ttk
import random

class MovieRecommendationSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Movie Recommendation System")
        self.master.geometry("600x400")

        self.movies = {
            "The Shawshank Redemption": ["Drama"],
            "The Godfather": ["Crime", "Drama"],
            "The Dark Knight": ["Action", "Crime", "Drama"],
            "Pulp Fiction": ["Crime", "Drama"],
            "Forrest Gump": ["Drama", "Romance"],
            "Inception": ["Action", "Adventure", "Sci-Fi"],
            "The Matrix": ["Action", "Sci-Fi"],
            "Goodfellas": ["Biography", "Crime", "Drama"],
            "The Silence of the Lambs": ["Crime", "Drama", "Thriller"],
            "Fight Club": ["Drama"],
            "Star Wars: Episode IV - A New Hope": ["Action", "Adventure", "Fantasy"],
            "The Lord of the Rings: The Fellowship of the Ring": ["Adventure", "Drama", "Fantasy"],
            "Schindler's List": ["Biography", "Drama", "History"],
            "Casablanca": ["Drama", "Romance", "War"],
            "Titanic": ["Drama", "Romance"],
        }

        self.genres = sorted(set(genre for genres in self.movies.values() for genre in genres))

        self.create_widgets()

    def create_widgets(self):
        # Frame for genre selection
        self.genre_frame = ttk.LabelFrame(self.master, text="Select Your Favorite Genres")
        self.genre_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Checkbuttons for genre selection
        self.genre_vars = {}
        for i, genre in enumerate(self.genres):
            var = tk.BooleanVar()
            ttk.Checkbutton(self.genre_frame, text=genre, variable=var).grid(row=i//3, column=i%3, sticky="w", padx=5, pady=2)
            self.genre_vars[genre] = var

        # Button to get recommendations
        self.recommend_button = ttk.Button(self.master, text="Get Recommendations", command=self.show_recommendations)
        self.recommend_button.pack(pady=10)

        # Frame for displaying recommendations
        self.recommendations_frame = ttk.LabelFrame(self.master, text="Recommended Movies")
        self.recommendations_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.recommendations_text = tk.Text(self.recommendations_frame, height=10, width=50, wrap=tk.WORD)
        self.recommendations_text.pack(padx=5, pady=5, fill="both", expand=True)

    def get_recommendations(self, user_genres):
        recommendations = []
        for movie, genres in self.movies.items():
            if any(genre in user_genres for genre in genres):
                recommendations.append(movie)
        return recommendations

    def show_recommendations(self):
        user_genres = [genre for genre, var in self.genre_vars.items() if var.get()]
        if not user_genres:
            self.recommendations_text.delete(1.0, tk.END)
            self.recommendations_text.insert(tk.END, "Please select at least one genre.")
            return

        recommendations = self.get_recommendations(user_genres)
        random.shuffle(recommendations)
        recommendations = recommendations[:5]  # Limit to 5 recommendations

        self.recommendations_text.delete(1.0, tk.END)
        if recommendations:
            for i, movie in enumerate(recommendations, 1):
                genres = ", ".join(self.movies[movie])
                self.recommendations_text.insert(tk.END, f"{i}. {movie} ({genres})\n\n")
        else:
            self.recommendations_text.insert(tk.END, "No movies found matching your preferences.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieRecommendationSystem(root)
    root.mainloop()

print("Movie Recommendation System has been implemented. Run this script to use the application!")