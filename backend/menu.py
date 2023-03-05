from sqlalchemy import SmallInteger
import datetime
import db

class OrmBase(db.DeclarativeBase):
    pass

class MenuItem(OrmBase):
    __tablename__ = 'items'
    
    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    name: db.Mapped[str] = db.mapped_column(db.String(100))

    hall: db.Mapped[str] = db.mapped_column(db.String(25))
    meal: db.Mapped[str] = db.mapped_column(db.String(10))
    date: db.Mapped[str] = db.mapped_column(db.Date)
    carbon_score: db.Mapped[datetime.date] = db.mapped_column(db.Integer())
    im_url: db.Mapped[str] = db.mapped_column(db.String(200))

    calories: db.Mapped[float] = db.mapped_column(db.Float())
    carbs: db.Mapped[float] = db.mapped_column(db.Float())
    chol: db.Mapped[float] = db.mapped_column(db.Float())
    fat: db.Mapped[float] = db.mapped_column(db.Float())
    fiber: db.Mapped[float] = db.mapped_column(db.Float())
    protein: db.Mapped[float] = db.mapped_column(db.Float())
    sat_fat: db.Mapped[float] = db.mapped_column(db.Float())
    sodium: db.Mapped[float] = db.mapped_column(db.Float())
    sugar: db.Mapped[float] = db.mapped_column(db.Float())
    trans_fat: db.Mapped[float] = db.mapped_column(db.Float())

    vegetarian: db.Mapped[SmallInteger] = db.mapped_column(db.SmallInteger())
    vegan: db.Mapped[SmallInteger] = db.mapped_column(db.SmallInteger())
    peanuts: db.Mapped[SmallInteger] = db.mapped_column(db.SmallInteger())
    tree_nuts: db.Mapped[SmallInteger] = db.mapped_column(db.SmallInteger())
    wheat: db.Mapped[SmallInteger] = db.mapped_column(db.SmallInteger())
    gluten: db.Mapped[SmallInteger] = db.mapped_column(db.SmallInteger())
    soy: db.Mapped[SmallInteger] = db.mapped_column(db.SmallInteger())
    sesame: db.Mapped[SmallInteger] = db.mapped_column(db.SmallInteger())
    dairy: db.Mapped[SmallInteger] = db.mapped_column(db.SmallInteger())
    eggs: db.Mapped[SmallInteger] = db.mapped_column(db.SmallInteger())
    shellfish: db.Mapped[SmallInteger] = db.mapped_column(db.SmallInteger())
    fish: db.Mapped[SmallInteger] = db.mapped_column(db.SmallInteger())
    halal: db.Mapped[SmallInteger] = db.mapped_column(db.SmallInteger())

    calcium_dv: db.Mapped[float] = db.mapped_column(db.Float())
    carbs_dv: db.Mapped[float] = db.mapped_column(db.Float())
    chol_dv: db.Mapped[float] = db.mapped_column(db.Float())
    fat_dv: db.Mapped[float] = db.mapped_column(db.Float())
    fiber_dv: db.Mapped[float] = db.mapped_column(db.Float())
    iron_dv: db.Mapped[float] = db.mapped_column(db.Float())
    potassium_dv: db.Mapped[float] = db.mapped_column(db.Float())
    sat_fat_dv: db.Mapped[float] = db.mapped_column(db.Float())
    sodium_dv: db.Mapped[float] = db.mapped_column(db.Float())
    vit_d_dv: db.Mapped[float] = db.mapped_column(db.Float())


    def __init__(self, values):
        for key, value in values.items():
            if (value is None) or (value == '' and key != 'im_url'):
                raise ValueError('{} should not be None'.format(key))
            setattr(self, key, value)

    def simplified(self):
        ret = { key: value for key, value in vars(self).items() if key[0] != '_' }
        ret['date'] = str(ret['date'])
        return ret

OrmBase.metadata.create_all(db.engine)
