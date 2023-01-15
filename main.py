import json

import init_django_orm  # noqa: F401

from db.models import Race, Skill, Player, Guild


def main() -> None:

    races = Race.objects
    skills = Skill.objects
    guilds = Guild.objects
    players = Player.objects

    for name, attributes in json.load(open("players.json", "r")).items():
        race_name = attributes["race"]["name"]
        race_description = attributes["race"]["description"]
        race_skills = attributes["race"]["skills"]

        try:
            guild_name = attributes["guild"]["name"]
            guild_description = attributes["guild"]["description"]
        except TypeError:
            pass

        if races.filter(name=race_name).exists() is False:
            races.create(
                name=race_name,
                description=race_description
            )

        if bool(attributes["guild"]) is True:
            if guilds.filter(name=guild_name).exists() is False:

                guilds.create(
                    name=guild_name,
                    description=guild_description
                )

        if bool(race_skills) is True:
            for skill in race_skills:
                if skills.filter(name=skill["name"]).exists() is False:

                    skills.create(
                        name=skill["name"],
                        bonus=skill["bonus"],
                        race=races.get(name=race_name)
                    )

        players.create(
            nickname=name,
            email=attributes["email"],
            bio=attributes["bio"],
            race=races.get(name=race_name),
        )

        if bool(attributes["guild"]) is True:
            players.filter(nickname=name).update(
                guild=guilds.get(name=guild_name)
            )


if __name__ == "__main__":
    main()
