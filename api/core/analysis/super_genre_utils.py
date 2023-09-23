class SuperGenreUtils:
    Pop = "Pop"
    Rock = "Rock"
    EDM = "EDM"
    Rap = "Rap"
    Schlager = "Schlager"
    ExtremeMetal = "Extreme Metal"
    Metal = "Metal"
    Classical = "Classical"
    Afro = "Afro"
    Others = "Others"
    
    SUPER_GENRES = [
        Pop, Rock, EDM, Rap, Schlager, ExtremeMetal, Metal, Classical, Afro,
        Others
    ]

    # Special handling because of overlap.
    # E.g. "dancehall" should be categorized as Afro, but contains "dance" so would be categorized as EDM
    ACCEPTED_EXACT_GENRES_BY_SUPER_GENRE = {
        Schlager: ["discofox"],
        Afro: ["dancehall"]
    }

    ACCEPTED_GENRE_SUBSTRINGS_BY_SUPER_GENRE = {
        Pop: ["pop", "new romantic", "wave", "girl group", "boy band"],
        Rock: ["rock", "post-grunge", "punk", "mellow gold"],
        EDM: [
            "edm", "dance", "house", "trance", "techno", "hands up", "hardstyle", "big room",
            "dubstep", "brostep", "complextro", "disco", "hi-nrg", "dancefloor", "drum and bass", "dnb",
            "jungle", "melbourne bounce", "indietronica"
        ],
        Rap: ["hip hop", "rap", "trap", "drill"],
        Schlager: ["schlager", "yodeling", "oktoberfest"],
        ExtremeMetal: ["black metal", "death metal", "melodeath"],
        Metal: ["metal", "neue deutsche harte", "industrial", "screamo", "emo", "nwobhm"],
        Classical: [
            "classical", "orchestra", "opera", "operetta", "romanticism", "romantic", "baroque",
            "tenor", "soprano", "orchestra", "early music", "canzone napoletana", "symphony"
        ],
        Afro: ["afro", "r&b", "soul", "reggae", "jazz", "funk", "urban", "dancehall"],
        Others: []
    }

    @staticmethod
    def get_super_genre_for_genre(genre):
        for super_genre in SuperGenreUtils.ACCEPTED_EXACT_GENRES_BY_SUPER_GENRE:
            accepted_exact_genres = SuperGenreUtils.ACCEPTED_EXACT_GENRES_BY_SUPER_GENRE[super_genre]
            if genre in accepted_exact_genres:
                return super_genre

        for super_genre in SuperGenreUtils.SUPER_GENRES:
            accepted_genre_substrings = SuperGenreUtils.ACCEPTED_GENRE_SUBSTRINGS_BY_SUPER_GENRE[super_genre]
            for accepted_genre_substring in accepted_genre_substrings:
                if accepted_genre_substring in genre:
                    return super_genre

        return SuperGenreUtils.Others

    @staticmethod
    def get_super_genres_for_genres(genres):
        if not genres:
            return [SuperGenreUtils.Others]

        unsorted_super_genres = []

        for genre in genres:
            super_genre = SuperGenreUtils.get_super_genre_for_genre(genre)
            if super_genre not in unsorted_super_genres:
                unsorted_super_genres.append(super_genre)

        sorted_super_genres = []
        for super_genre in SuperGenreUtils.SUPER_GENRES:
            if super_genre in unsorted_super_genres:
                sorted_super_genres.append(super_genre)

        return sorted_super_genres
