from all_functions import *

def plot_unicast_tp_cdfs(files, axes):
    for file in files:
        df = pd.read_csv(file)
        combined_df = pd.concat([ df['run_1_throughput'], df['run_2_throughput'], df['run_3_throughput'] ])
        if 'sub_0' in file:
            plot_cdf('Unicast Sub 0 Run 1', df['run_1_throughput'], axes[0], greens[6], 'normal')
            plot_cdf('Unicast Sub 0 Run 2', df['run_2_throughput'], axes[0], greens[3], 'normal')
            plot_cdf('Unicast Sub 0 Run 3', df['run_3_throughput'], axes[0], greens[0], 'normal')
            plot_cdf('Unicast Sub 0 Avg.', combined_df, axes[0], greens[0], 'average')
        elif 'sub_1' in file:
            plot_cdf('Unicast Sub 1 Run 1', df['run_1_throughput'], axes[1], greens[6], 'normal')
            plot_cdf('Unicast Sub 1 Run 2', df['run_2_throughput'], axes[1], greens[3], 'normal')
            plot_cdf('Unicast Sub 1 Run 3', df['run_3_throughput'], axes[1], greens[0], 'normal')
            plot_cdf('Unicast Sub 1 Avg.', combined_df, axes[1], greens[0], 'average')
        elif 'sub_2' in file:
            plot_cdf('Unicast Sub 2 Run 1', df['run_1_throughput'], axes[2], greens[6], 'normal')
            plot_cdf('Unicast Sub 2 Run 2', df['run_2_throughput'], axes[2], greens[3], 'normal')
            plot_cdf('Unicast Sub 2 Run 3', df['run_3_throughput'], axes[2], greens[0], 'normal')
            plot_cdf('Unicast Sub 2 Avg.', combined_df, axes[2], greens[0], 'average')

def plot_multicast_tp_cdfs(files, axes):
    for file in files:
        df = pd.read_csv(file)
        combined_df = pd.concat([ df['run_1_throughput'], df['run_2_throughput'], df['run_3_throughput'] ])
        if 'sub_0' in file:
            plot_cdf('Multicast Sub 0 Run 1', df['run_1_throughput'], axes[0], reds[6], 'normal')
            plot_cdf('Multicast Sub 0 Run 2', df['run_2_throughput'], axes[0], reds[3], 'normal')
            plot_cdf('Multicast Sub 0 Run 3', df['run_3_throughput'], axes[0], reds[0], 'normal')
            plot_cdf('Multicast Sub 0 Avg.', combined_df, axes[0], reds[0], 'average')
        elif 'sub_1' in file:
            plot_cdf('Multicast Sub 1 Run 1', df['run_1_throughput'], axes[1], reds[6], 'normal')
            plot_cdf('Multicast Sub 1 Run 2', df['run_2_throughput'], axes[1], reds[3], 'normal')
            plot_cdf('Multicast Sub 1 Run 3', df['run_3_throughput'], axes[1], reds[0], 'normal')
            plot_cdf('Multicast Sub 1 Avg.', combined_df, axes[1], reds[0], 'average')
        elif 'sub_2' in file:
            plot_cdf('Multicast Sub 2 Run 1', df['run_1_throughput'], axes[2], reds[6], 'normal')
            plot_cdf('Multicast Sub 2 Run 2', df['run_2_throughput'], axes[2], reds[3], 'normal')
            plot_cdf('Multicast Sub 2 Run 3', df['run_3_throughput'], axes[2], reds[0], 'normal')
            plot_cdf('Multicast Sub 2 Avg.', combined_df, axes[2], reds[0], 'average')

def demonstrate_ucast_vs_mcast():
    xs = range(0, 100)
    ucast_ys = [2 * x for x in xs]
    mcast_ys = [x + 1 for x in xs]

    fig, ax = plt.subplots(figsize=(20, 10))
    _ = ax.plot(xs, ucast_ys, label="Unicast: $y = 2x$")
    _ = ax.plot(xs, mcast_ys, label="Multicast: $y = x + 1$")
    ax.set_xlim(xmin=0, xmax=100)
    ax.set_ylim(ymin=0, ymax=100)
    _ = ax.legend()

def plot_summary_table(ucast, mcast):
    # Get unicast latency files
    headings = ["", "", "Unicast", "", "", "Multicast", ""]
    runs = ["Runs", 1, 2, 3, 1, 2, 3]
    metric_count = ["No. of Measurements".title()]
    averages = ["averages".title()]
    stds = ["stds".title()]
    variances = ["variances".title()]
    mins = ["mins".title()]
    maxs = ["maxs".title()]
    lower_quartiles = ["lower_quartiles".title().replace("_", " ")]
    mid_quartiles = ["mid_quartiles".title().replace("_", " ")]
    upper_quartiles = ["upper_quartiles".title().replace("_", " ")]

    df = pd.read_csv(ucast)
    for col in df.columns[1:4]:
        metric_count.append(format_number(df[col].count()))
        averages.append(format_number(df[col].mean()))
        stds.append(format_number(df[col].std()))
        variances.append(format_number(df[col].var()))
        mins.append(format_number(df[col].min()))
        maxs.append(format_number(df[col].max()))
        lower_quartiles.append(format_number(df[col].quantile(.25)))
        mid_quartiles.append(format_number(df[col].quantile(.5)))
        upper_quartiles.append(format_number(df[col].quantile(.75)))

    df = pd.read_csv(mcast)
    for col in df.columns[1:4]:
        metric_count.append(format_number(df[col].count()))
        averages.append(format_number(df[col].mean()))
        stds.append(format_number(df[col].std()))
        variances.append(format_number(df[col].var()))
        mins.append(format_number(df[col].min()))
        maxs.append(format_number(df[col].max()))
        lower_quartiles.append(format_number(df[col].quantile(.25)))
        mid_quartiles.append(format_number(df[col].quantile(.5)))
        upper_quartiles.append(format_number(df[col].quantile(.75)))

    rows = [runs, metric_count, averages, stds, variances, mins, maxs, lower_quartiles, mid_quartiles, upper_quartiles]

    # Get summary data for unicast per run
    fig, ax = plt.subplots(dpi=200)
    ax.set_axis_off()
    table = plot_table(ax, headings, rows)
    table.auto_set_font_size(False)
    table.set_fontsize(4)
    plt.tight_layout()