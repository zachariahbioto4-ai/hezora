from django.core.management.base import BaseCommand
from books.models import Book

class Command(BaseCommand):
    help = 'Seeds the database with standard premium BookBase books'

    def handle(self, *args, **kwargs):
        books_data = [
            {
                "title": "The Psychology of Money",
                "author": "Morgan Housel",
                "cover_url": "[https://images-na.ssl-images-amazon.com/images/I/71g2ednj0JL.jpg](https://images-na.ssl-images-amazon.com/images/I/71g2ednj0JL.jpg)",
                "category": "Finance",
                "rating": 4.8,
                "pages": 250,
                "ratings_count": "1,240",
                "reviews_count": "320",
                "is_recommended": True,
                "color_gradient": "from-emerald-800 to-teal-900",
                "description": "Timeless lessons on wealth, greed, and happiness. Doing well with money isn't necessarily about what you know. It's about how you behave."
            },
            {
                "title": "How Innovation Works",
                "author": "Matt Ridley",
                "cover_url": "[https://images-na.ssl-images-amazon.com/images/I/81dE8gZor6L.jpg](https://images-na.ssl-images-amazon.com/images/I/81dE8gZor6L.jpg)",
                "category": "Science",
                "rating": 4.7,
                "pages": 352,
                "ratings_count": "942",
                "reviews_count": "180",
                "is_recommended": True,
                "color_gradient": "from-amber-500 to-yellow-600",
                "description": "Innovation is the main event of the modern age, the reason we experience compound growth in living standards. Ridley discusses how it occurs and why it must be sustained."
            },
            {
                "title": "Company of One",
                "author": "Paul Jarvis",
                "cover_url": "[https://images-na.ssl-images-amazon.com/images/I/71gY-8GqKDL.jpg](https://images-na.ssl-images-amazon.com/images/I/71gY-8GqKDL.jpg)",
                "category": "Business",
                "rating": 4.8,
                "pages": 320,
                "ratings_count": "643",
                "reviews_count": "110",
                "is_recommended": True,
                "color_gradient": "from-slate-700 to-slate-950",
                "description": "Company of One offers a refreshingly original business strategy that's focused on a commitment to being better instead of bigger. Staying small provides you with the freedom to pursue more meaningful life projects."
            },
            {
                "title": "Stupore E Tremori",
                "author": "Amélie Nothomb",
                "cover_url": "[https://images-na.ssl-images-amazon.com/images/I/81xU7vP-Z9L.jpg](https://images-na.ssl-images-amazon.com/images/I/81xU7vP-Z9L.jpg)",
                "category": "Drama",
                "rating": 4.5,
                "pages": 140,
                "ratings_count": "452",
                "reviews_count": "95",
                "is_recommended": True,
                "color_gradient": "from-orange-800 to-amber-950",
                "description": "A satirical novel describing the corporate culture of a Japanese company through the eyes of a young Western woman trying to integrate into the hierarchy."
            },
            {
                "title": "The Bees",
                "author": "Laline Paull",
                "cover_url": "[https://images-na.ssl-images-amazon.com/images/I/81T6YV9Zp8L.jpg](https://images-na.ssl-images-amazon.com/images/I/81T6YV9Zp8L.jpg)",
                "category": "Sci-Fi",
                "rating": 4.6,
                "pages": 352,
                "ratings_count": "823",
                "reviews_count": "142",
                "is_recommended": False,
                "color_gradient": "from-zinc-900 to-slate-800",
                "description": "A thrilling and highly original dystopian novel set within a beehive, capturing a totalitarian world where only the Queen is allowed to breed."
            },
            {
                "title": "Real Help",
                "author": "Ayodeji Awosika",
                "cover_url": "[https://images-na.ssl-images-amazon.com/images/I/61rS-y79fUL.jpg](https://images-na.ssl-images-amazon.com/images/I/61rS-y79fUL.jpg)",
                "category": "Education",
                "rating": 4.9,
                "pages": 290,
                "ratings_count": "340",
                "reviews_count": "88",
                "is_recommended": False,
                "color_gradient": "from-blue-900 to-indigo-950",
                "description": "An honest guide to self-improvement. It covers the psychological barriers to success, focusing on practical actions instead of empty motivational speech."
            },
            {
                "title": "The Fact of a Body",
                "author": "Alexandria Marzano-Lesnevich",
                "cover_url": "[https://images-na.ssl-images-amazon.com/images/I/81rF615CgCL.jpg](https://images-na.ssl-images-amazon.com/images/I/81rF615CgCL.jpg)",
                "category": "Drama",
                "rating": 4.8,
                "pages": 326,
                "ratings_count": "1,105",
                "reviews_count": "210",
                "is_recommended": False,
                "color_gradient": "from-red-950 to-stone-900",
                "description": "Part memoir, part true crime, the author investigates a murder trial while confronting traumatic details from her own personal past."
            },
            {
                "title": "The Room",
                "author": "Jonas Karlsson",
                "cover_url": "[https://images-na.ssl-images-amazon.com/images/I/71N-WfU7KXL.jpg](https://images-na.ssl-images-amazon.com/images/I/71N-WfU7KXL.jpg)",
                "category": "Fantasy",
                "rating": 4.4,
                "pages": 192,
                "ratings_count": "310",
                "reviews_count": "67",
                "is_recommended": False,
                "color_gradient": "from-teal-900 to-cyan-950",
                "description": "A short, hilarious Kafkaesque office comedy about a man who discovers a secret, pristine, unoccupied room in his office building that no one else can see."
            },
            {
                "title": "Through the Breaking",
                "author": "Cate Emond",
                "cover_url": "[https://images-na.ssl-images-amazon.com/images/I/81I3i7qMvTL.jpg](https://images-na.ssl-images-amazon.com/images/I/81I3i7qMvTL.jpg)",
                "category": "Geography",
                "rating": 4.3,
                "pages": 280,
                "ratings_count": "150",
                "reviews_count": "35",
                "is_recommended": False,
                "color_gradient": "from-emerald-950 to-emerald-900",
                "description": "An adventurous tale exploring deep geographic landscapes, personal endurance, and discovering community in the most remote regions."
            }
        ]

        self.stdout.write("Clearing existing books database...")
        Book.objects.all().delete()

        self.stdout.write("Seeding clean BookBase database items...")
        for book_info in books_data:
            Book.objects.create(**book_info)

        self.stdout.write(self.style.SUCCESS('Successfully seeded BookBase database items!'))
