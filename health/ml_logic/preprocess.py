import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix



def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    def compress(df, **kwargs):
        """
        Reduces the size of the DataFrame by downcasting numerical columns
        """
        input_size = df.memory_usage(index=True).sum()/ 1024**2
        print("old dataframe size: ", round(input_size,2), 'MB')

        in_size = df.memory_usage(index=True).sum()

        for t in ["float", "integer"]:
            l_cols = list(df.select_dtypes(include=t))

            for col in l_cols:
                df[col] = pd.to_numeric(df[col], downcast=t)

        out_size = df.memory_usage(index=True).sum()
        ratio = (1 - round(out_size / in_size, 2)) * 100

        print("optimized size by {} %".format(round(ratio,2)))
        print("new DataFrame size: ", round(out_size / 1024**2,2), " MB")

        return df

    ## caminho
    file = 'filtered_columns_LLCP2023.csv'
    df   = pd.read_csv(file)

    ## DataFrame shape
    print(df.shape)

    df = compress(df, verbose=True)

    ## overview - missing values
    missing_values        = df.isnull().sum()
    missing_values_sorted = missing_values.sort_values(ascending=False)
    print(missing_values_sorted.head(20))

    ## categorical variables
    categorical_col = ['_PACAT3', '_RFHYPE6', '_RFCHOL3', '_MICHD', '_LTASTH1',
                    '_AGEG5YR', '_DRDXAR2', '_BMI5CAT', '_EDUCAG', '_INCOMG1',
                    'SEXVAR', 'GENHLTH', 'EXERANY2', 'CHECKUP1', 'EXRACT12',
                    'EXRACT22', 'CVDINFR4', 'CVDCRHD4', 'CVDSTRK3', 'CHCOCNC1',
                    'CHCCOPD3', 'ADDEPEV3', 'CHCKDNY2', 'DIABETE4',
                    'DECIDE', 'DIFFALON', '_PHYS14D', '_MENT14D', 'ACTIN13_', '_PAINDX3'
                    ]

    ## replacing 88 to zero and the others to NaN
    df[categorical_col] = df[categorical_col].replace(88.0, 0)
    df[categorical_col] = df[categorical_col].replace([77.0, 777.0, 7777.0, 888.0, 99.0, 999.0], np.nan)

    #_PACAT3, _INCOMG1, _PAINDX3  NAO tiramos o 9 para nao criar noise!!!!!!!!!!
    ## 9 = refused, don't know
    cat_col_nan = ["_RFCHOL3", "_LTASTH1", "GENHLTH", "EXERANY2",
                "CHECKUP1", "CVDINFR4", "CVDCRHD4", "CVDSTRK3", "CHCOCNC1", "CHCCOPD3",
                "ADDEPEV3", "CHCKDNY2", "DIABETE4", "DECIDE", "DIFFALON", "_PHYS14D",
                "_MENT14D", "_RFHYPE6", "_EDUCAG"]
    df[cat_col_nan] = df[cat_col_nan].replace(9.0, np.nan)


    ## 7 = don't know
    var_dontknow = ["GENHLTH", "DIABETE4", "EXERANY2", "CHECKUP1", "CVDINFR4", "CVDSTRK3", "CHCOCNC1", "CHCCOPD3", "ADDEPEV3", "CHCKDNY2", "DECIDE", "DIFFALON"]
    df[var_dontknow] = df[var_dontknow].replace(7.0, np.nan)

    ## selecting numeric columns
    numerical_col = df.drop(columns=categorical_col)

    ## columns where 77/88/888/999 should NOT be NaN (part of the dataset - manually verified (vrf))
    num_col_vrf = ["HTM4", "WTKG3", "EXERHMM1", "MAXVO21_", "STRFREQ_", "PA3MIN_"]

    ## filtering numeric columns where 77/88/888 should be NaN
    num_col_nan = numerical_col.drop(columns=num_col_vrf)

    ## replacing 88 to zero and the others to NaN
    df[num_col_nan.columns] = df[num_col_nan.columns].replace(88.0, 0)
    df[num_col_nan.columns] = df[num_col_nan.columns].replace([77.0, 777.0, 7777.0, 888.0, 99.0, 999.0], np.nan)

    ## 99900.0 = NaN
    df[["MAXVO21_", "STRFREQ_"]] = df[["MAXVO21_", "STRFREQ_"]].replace([99900.0], np.nan)

    ## alterando 1=yes, 2=no
    mapeamento_RFCHOL3  = {1:2, 2:1}
    mapeamento_LTASTH1  = {1:2, 2:1}
    mapeamento_DIABETE4 = {1:1, 2:1, 3:2, 4:2} # gravidas... viraram yes

    # Aplicando o mapeamento
    df['_RFCHOL3'] = df['_RFCHOL3'].map(mapeamento_RFCHOL3)
    df['_LTASTH1'] = df['_LTASTH1'].map(mapeamento_LTASTH1)
    df['DIABETE4'] = df['DIABETE4'].map(mapeamento_DIABETE4)

    cat_imputer = SimpleImputer(strategy='most_frequent')

    ## imputer - numerical variables (using "mean")
    num_imputer = SimpleImputer(strategy='mean')

    ## ColumnTransformer - transforming each column
    preprocessor = ColumnTransformer(transformers=[('num', num_imputer, numerical_col.columns),
                                                ('cat', cat_imputer, df[categorical_col].columns)
                                                ]
                                    )

    ## Pipeline - applying ColumnTransformer
    pipeline   = Pipeline(steps=[('preprocessor', preprocessor)])
    df_imputed = pipeline.fit_transform(df)

    ## columns names
    feature_names = pipeline.named_steps['preprocessor'].get_feature_names_out()

    ## removing prefixes 'num__' and 'cat__'
    feature_names = [name.replace('num__', '').replace('cat__', '') for name in feature_names]

    ## converting to DataFrame
    df_imputed = pd.DataFrame(df_imputed, columns=feature_names)

    # 1. Aplicação do OrdinalEncoder nas colunas ordinais

    # Definir as categorias específicas para cada variável ordinal
    ordinal_cols = ['_PACAT3', '_AGEG5YR', '_BMI5CAT', '_EDUCAG', '_INCOMG1',
                    'GENHLTH', 'CHECKUP1', '_PHYS14D', '_MENT14D']

    categories = [
        [1, 2, 3, 4, 9],                                  # _PACAT3 (Highly Active, Active, Insufficiently Active, Inactive)
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],  # _AGEG5YR (age groups from 1 to 14)
        [1, 2, 3, 4],                                     # _BMI5CAT (underweight, normal, overweight, obese)
        [1, 2, 3, 4],                                     # _EDUCAG (education levels)
        [1, 2, 3, 4, 5, 6, 7, 8, 9],                      # _INCOMG1 (income groups from 1 to 8)
        [1, 2, 3, 4, 5],                                  # GENHLTH (health levels from Excellent to Poor)
        [1, 2, 3, 4, 7, 8, 9],                            # CHECKUP1 (time since last checkup)
        [1, 2, 3],                                        # _PHYS14D (0 days, 1-13 days, 14-30 days)
        [1, 2, 3]                                         # _MENT14D (0 days, 1-13 days, 14-30 days)
    ]

    # Aplicar o OrdinalEncoder com as categorias fornecidas
    ordinal_encoder = OrdinalEncoder(categories=categories).set_output(transform="pandas")

    # Transformar as colunas ordinais
    df_transformed = df_imputed.copy() #cria uma cópia com as colunas numéricas também. NUMERICA + CATEGORICA
    df_transformed[ordinal_cols] = ordinal_encoder.fit_transform(df_imputed[ordinal_cols])

    # 2. Aplicação do OneHotEncoder nas colunas nominais

    # Definir as colunas nominais (sem ordem)
    drop_cols = ordinal_cols + numerical_col.columns.tolist()
    nominal_cols = df_imputed.drop(columns=drop_cols).columns

    # Aplicando One-Hot Encoding em todas as colunas nominais
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore').set_output(transform="pandas")

    # Codificar as colunas nominais
    encoded_data = encoder.fit_transform(df_imputed[nominal_cols])

    # Concatenando os dados transformados (ordinais + nominais codificados)
    df_final = pd.concat([df_transformed, encoded_data], axis=1)

    # Exibindo o DataFrame final
    print(df_final.head(20))

    # Normalização
    scaler = StandardScaler().set_output(transform="pandas")

    normalized_data = scaler.fit_transform(df_final)

    normalized_dataframe = pd.DataFrame(normalized_data)

    ## features, target
    X = normalized_dataframe.drop(columns=['GENHLTH', 'GENHLTH_Engineered'])
    y = normalized_dataframe['GENHLTH_Engineered']

    # XG Boost
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    param_dist = {
        'max_depth': [3, 5],
        'learning_rate': [0.1],
        'n_estimators': [50, 100],
        'colsample_bytree': [0.7],
        'subsample': [0.8],
        'gamma': [0, 0.1],
        'min_child_weight': [1, 5]
    }

    xgb_model = XGBClassifier(random_state=42)

    random_search = RandomizedSearchCV(
        estimator=xgb_model,
        param_distributions=param_dist,
        n_iter=10,
        scoring='f1_weighted',
        cv=2,
        n_jobs=-1,
        random_state=42,
        verbose=2
    )

    random_search.fit(X_train, y_train)

    print("Melhores hiperparâmetros:", random_search.best_params_)

    best_xgb = random_search.best_estimator_

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    best_xgb.fit(X_train, y_train)

    y_pred_best = best_xgb.predict(X_test)

    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_best))
    print("\nClassification Report:\n", classification_report(y_test, y_pred_best))

    accuracy_best = accuracy_score(y_test, y_pred_best)
    print(f"\nAccuracy com os melhores hiperparâmetros: {accuracy_best:.2f}")

    return df_final
