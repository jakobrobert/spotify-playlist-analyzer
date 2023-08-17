class SuperGenreUtils:
    Pop = "Pop"
    Rock = "Rock"
    EDM = "EDM"
    HipHopOrRap = "Hip Hop / Rap"
    Schlager = "Schlager"
    ExtremeMetal = "Extreme Metal"
    Metal = "Metal"
    Classical = "Classical"
    Afro = "Afro"
    Others = "Others"
    
    SUPER_GENRES = [
        Pop, Rock, EDM, HipHopOrRap, Schlager,
        ExtremeMetal, Metal, Classical, Afro,
        Others
    ]

    ACCEPTED_GENRE_SUBSTRINGS_BY_SUPER_GENRE = {
        Pop: ["pop", "new romantic", "wave", "girl group", "boy band"],
        Rock: ["rock", "post-grunge", "punk", "mellow gold"],
        EDM: [
            "edm", "dance", "house", "trance", "techno", "hands up", "hardstyle", "big room",
            "dubstep", "brostep", "complextro", "disco", "hi-nrg", "dancefloor", "drum and bass", "dnb",
            "jungle", "melbourne bounce"
        ],
        HipHopOrRap: ["hip hop", "rap", "trap", "drill"],
        Schlager: ["schlager"],
        ExtremeMetal: ["black metal", "death metal", "melodeath"],
        Metal: ["metal", "neue deutsche harte", "industrial", "screamo", "emo", "nwobhm"],
        Classical: ["classical", "orchestra", "opera"],
        Afro: ["afro", "r&b", "soul", "reggae", "funk", "urban", "dancehall"],
        Others: []
    }

    @staticmethod
    def get_super_genre_for_genre(genre):
        for super_genre in SuperGenreUtils.SUPER_GENRES:
            accepted_genre_substrings = SuperGenreUtils.ACCEPTED_GENRE_SUBSTRINGS_BY_SUPER_GENRE[super_genre]
            for accepted_genre_substring in accepted_genre_substrings:
                if accepted_genre_substring in genre:
                    return super_genre

        return SuperGenreUtils.Others
