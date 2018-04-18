
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from data.data_processing import *
from analysis.user_elite_analysis import *

if __name__ == '__main__':

    # step 1 gen process_data
    # extract_user_basic_attributes()
    # extract_user_average_review_lengths()
    # extract_user_reading_levels()
    # extract_user_tip_counts()
    # extract_user_pageranks()

    # step 2 combine data
    # combine_all_user_data()
    # create_training_and_test_sets(fraction_for_training=0.8)

    # step 3 analyze data
    # train_random_forest_elite_status_classifier()

    # step 4 testing
    # test_elite_status_classifier(
    #     ModelClass=RandomForestClassifier,
    #     attributes=RANDOM_FOREST_USER_ATTRIBUTES,
    #     model_arguments=RANDOM_FOREST_ARGUMENTS,
    #     balance_training_set=True, # Optional: whether the model should be trained on equally many Elite and non-Elite users
    #     balance_test_set=True      # Optional: whether the model should be tested on equally many Elite and non-Elite users
    # )

    # step 5 Visualize Social Network Properties
    # from analysis.user_graph_analysis import *
    # analyze_user_graph(
    #     show_degree_histogram=True,
    #     show_pagerank_histogram=True
    # )


    pass