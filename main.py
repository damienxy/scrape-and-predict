import pandas as pd  # type: ignore

from collect import collect_artists
from analysis import make_model, predict_artist

import cfg


if __name__ == "__main__":
    print(cfg.messages['welcome'])
    # Initialize
    df = pd.DataFrame(columns=cfg.df_columns)
    # Create corpus
    df = collect_artists(df, cfg.messages['provide_artist'])

    if len(df.index) >= 10:
        # Train model
        model = make_model(df)
        # Predict artists
        predict_artist(model)
    else:
        print(cfg.messages['not_enough_data'])
