from .init import curs, IntegrityError
from model.creature import Creature
from errors import Missing, Duplicate


curs.execute("""create table if not exists creature(
            name text primary key,
            description text,
            country text,
            area text,
            aka text
            )""")


def row_to_model(row: tuple) -> Creature:
    name, description, country, area, aka = row
    return Creature(
        name=name,
        description=description,
        country=country,
        area=area,
        aka=aka
        )


def model_to_dict(creature: Creature) -> dict:
    return creature.dict()


def get_one(name: str) -> Creature:
    qry = "select * from creature where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Creature.{name} not found")


def get_all(name: str) -> list[Creature]:
    qry = "select * from creature"
    curs.execute(qry)
    rows = list(curs.fetchall())
    return [row_to_model(row) for row in rows]


def create(creature: Creature):
    if not creature:
        return None

    qry = """insert into creature values
        (:name, :description, :country, :area, :aka)"""
    params = model_to_dict(creature)
    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(
            msg=f"Creature {creature.name} not found"
        )
    return get_one(creature.name)


def modify(creature: Creature):
    if not creature:
        return None

    qry = """update creature
                set country=:country,
                name=:name,
                description=:description,
                area=:area,
                aka=:aka
            where name=:name_orig"""
    params = model_to_dict(creature)
    params["name_orig"] = creature.name
    curs.execute(qry, params)
    if curs.rowcount == 1:
        return get_one(creature.name)
    else:
        raise Missing(msg=f"Creature {creature.name} not found")


def delete(name: str):
    if not name:
        return False
    qry = "delete from creature where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"Creature {name} not found")
    return True
