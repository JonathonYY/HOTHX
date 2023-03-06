import db

class OrmBase(db.DeclarativeBase):
    pass

class MenuItem(OrmBase):
    __tablename__ = 'items'
    
    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    name: db.Mapped[str] = db.mapped_column(db.String(100))

    hall: db.Mapped[str] = db.mapped_column(db.String(25))
    meal: db.Mapped[str] = db.mapped_column(db.String(10))
    carbon_score: db.Mapped[str] = db.mapped_column(db.Integer())
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
        return { key: value for key, value in vars(self).items() }

OrmBase.metadata.create_all(db.engine)
