import numpy as np
import tests
import analysis
import utilities
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

models = utilities.generate_list_models(10)

#########################################################################
# compare the monotonicity measure for three natural language quantifiers

# all = np.all(models, axis=1)
#
# card = np.sum(models, axis=1)
# less_than_2_more_than_5 = (card <= 2) | (card >= 5)
#
# even_number = card % 2 == 0
#
# with np.printoptions(threshold=np.inf):
#     print(all)
#     print(less_than_2_more_than_5)
#     print(even_number)
#
# print("All: ", tests.measure_monotonicity(models, all))
# print("Less than 2 or more than 5: ", tests.measure_monotonicity(models, less_than_2_more_than_5))
# print("Even: ", tests.measure_monotonicity(models, even_number))

# plot the mean of monotonicity measure by number of epochs and bottleneck size

# fn_pattern = '/exports/eddie/scratch/s1569804/*shuffle_input-False*/quantifiers.csv'
fn_pattern = './*/quantifiers.csv'
df = analysis.get_summaries(fn_pattern)


print(df.columns)
df = df.filter(regex='bottleneck|num_epochs|num_trial|monotonicity|generation').astype({
    "bottleneck": int,
    "num_epochs": int,
    "generation": int
})

# unpivots the monotonicity columns
df = pd.melt(
    df,
    id_vars=["num_epochs", "num_trial", "generation", "bottleneck"],
    value_vars=['monotonicity_0', 'monotonicity_1', 'monotonicity_2', 'monotonicity_3',
        'monotonicity_4', 'monotonicity_5', 'monotonicity_6', 'monotonicity_7',
        'monotonicity_8', 'monotonicity_9'],
    value_name="monotonicity"
)

# rename columns for figure legen
df.rename(columns={
    "bottleneck": "Bottleneck",
    "num_epochs": "Epochs"
}, inplace=True)


#########################################
# simple single plot (but visually messy)

# ax = sns.lineplot(
#     x='generation',
#     y='monotonicity',
#     hue='Bottleneck',
#     style='Epochs',
#     data=df,
#     # specify as many colors as there are elements of the hue, otherwise it add uninstantiated values in the legend
#     # see: https://stackoverflow.com/questions/51525284/the-hue-parameter-in-seaborn-relplot-skips-an-integer-when-given-numerical-d
#     palette=["m", "g", "y", "r"]
# )
#
# plt.ylim(0, 1)
# plt.xlabel("Generation")
# plt.ylabel("Monotonicity")
#
# plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
# plt.tight_layout()
#
# ax.get_figure().savefig('./evolution_monotonicity_by_training_size.pdf')

################################################
# same plot but num of epochs in different plots
sns.set(font_scale=1.2)
g = sns.FacetGrid(data=df, col='Epochs', hue='Bottleneck', palette="Blues")
g = (g.map(sns.lineplot, 'generation', 'monotonicity')
     .add_legend()
     .set_axis_labels("Generation", "Monotonicity"))
g.savefig('./evolution_monotonicity_by_training_size.pdf')