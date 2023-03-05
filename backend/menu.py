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

    calories: db.Mapped[int] = db.mapped_column(db.Integer())
    carbs: db.Mapped[int] = db.mapped_column(db.Integer())
    chol: db.Mapped[int] = db.mapped_column(db.Integer())
    fat: db.Mapped[int] = db.mapped_column(db.Integer())
    fiber: db.Mapped[int] = db.mapped_column(db.Integer())
    protein: db.Mapped[int] = db.mapped_column(db.Integer())
    sat_fat: db.Mapped[int] = db.mapped_column(db.Integer())
    sodium: db.Mapped[int] = db.mapped_column(db.Integer())
    sugar: db.Mapped[int] = db.mapped_column(db.Integer())

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

    def simplified(self):
        return { key: value for key, value in vars(self).items() }

OrmBase.metadata.create_all(db.engine)
