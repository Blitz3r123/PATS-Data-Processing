from all_functions import * 

def ucast_vs_mcast_lat_boxplots():
    # ---------------------------------------------------------------------------- #
    #                                File Gathering                                #
    # ---------------------------------------------------------------------------- #
    lats = [file for file in get_files("data/v2/set_2") if "average_latencies" in file]
    ucast_lats = {
        "10p10s": [file for file in lats if "10p_10s" in file and "unicast" in file],
        "25p25s": [file for file in lats if "25p_25s" in file and "unicast" in file],
        "50p50s": [file for file in lats if "50p_50s" in file and "unicast" in file],
        "75p75s": [file for file in lats if "75p_75s" in file and "unicast" in file]
    }
    mcast_lats = {
        "10p10s": [file for file in lats if "10p_10s" in file and "multicast" in file],
        "25p25s": [file for file in lats if "25p_25s" in file and "multicast" in file],
        "50p50s": [file for file in lats if "50p_50s" in file and "multicast" in file],
        "75p75s": [file for file in lats if "75p_75s" in file and "multicast" in file]
    }

    # ---------------------------------------------------------------------------- #
    #                                  Data Frames                                 #
    # ---------------------------------------------------------------------------- #
    ucast_dfs = {}
    mcast_dfs = {}
    for item in ucast_lats:
        ucast_dfs[item] = (remove_infs_nans(pd.read_csv(ucast_lats[item][0])["run_1_latency"]) / 1000).to_frame('latency')['latency']
        mcast_dfs[item] = (remove_infs_nans(pd.read_csv(mcast_lats[item][0])["run_1_latency"]) / 1000).to_frame('latency')['latency']
    
    combined = {
        "u10p10s": ucast_dfs["10p10s"],
        "m10p10s": mcast_dfs["10p10s"],
        "u25p25s": ucast_dfs["25p25s"],
        "m25p25s": mcast_dfs["25p25s"],
        "u50p50s": ucast_dfs["50p50s"],
        "m50p50s": mcast_dfs["50p50s"],
        "u75p75s": ucast_dfs["75p75s"],
        "m75p75s": mcast_dfs["75p75s"]
    }
    
    # ---------------------------------------------------------------------------- #
    #                                    Figure                                    #
    # ---------------------------------------------------------------------------- #
    # fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(30, 5))
    fig = plt.figure(figsize=(30, 20))
    fig.suptitle("Unicast vs Multicast for Varying Participants Latency Boxplots", fontsize=15, fontweight="bold")
    
    # ---------------------------------------------------------------------------- #
    #                                     Grids                                    #
    # ---------------------------------------------------------------------------- #
    grid = plt.GridSpec(4, 4, figure=fig)
    
    top0 = plt.subplot(grid[0, 0])
    top1 = plt.subplot(grid[0, 1])
    top2 = plt.subplot(grid[0, 2])
    top3 = plt.subplot(grid[0, 3])
    
    main = plt.subplot(grid[1:4, 0:4])
    
    # ---------------------------------------------------------------------------- #
    #                                   Box Plots                                  #
    # ---------------------------------------------------------------------------- #
    for item in ucast_dfs:
        if "10p10s" in item:
            title = "10P + 10S Unicast vs Multicast Latency Boxplots"
            ax = top0
        elif "25p25s" in item:
            title = "25P + 25S Unicast vs Multicast Latency Boxplots"
            ax = top1
        elif "50p50s" in item:
            title = "50P + 50S Unicast vs Multicast Latency Boxplots"
            ax = top2
        elif "75p75s" in item:
            title = "75P + 75S Unicast vs Multicast Latency Boxplots"
            ax = top3
            
        new_dict = {"ucast": ucast_dfs[item], "mcast": mcast_dfs[item]}
        box = ax.boxplot(new_dict.values(), showfliers=False, patch_artist=True)
        
        colors = [greens[0], reds[0], greens[0], reds[0], greens[0], reds[0], greens[0], reds[0]]
        for patch, color in zip(box['boxes'], colors):
            patch.set_facecolor(color)

        ax.set_xticklabels(["Unicast", "Multicast"])
        ax.set_title(title)
        ax.grid(axis="y", color="#ddd")
        ax.spines.right.set_visible(False)
        ax.spines.top.set_visible(False)
        ax.spines.bottom.set_color("#999")
        ax.spines.left.set_color("#999")
        ax.set_ylabel("Latency (ms)")
        ax.set_ylim(ymin=0)
        
    main_box = main.boxplot(combined.values(), showfliers=False, patch_artist=True)
    for patch, color in zip(main_box['boxes'], colors):
            patch.set_facecolor(color)
    main.set_yscale("log")
    main.grid(axis="y", color="#ddd")
    main.spines.top.set_visible(False)
    main.spines.right.set_visible(False)
    main.spines.bottom.set_color("#999")
    main.spines.left.set_color("#999")
    main.set_ylabel("Latency (ms)")
    main.set_title("Combined Unicast vs Multicast Latency Boxplots")
    main.set_xticklabels([
        "10P10S Unicast",
        "10P10S Multicast",
        "25P25S Unicast",
        "25P25S Multicast",
        "50P50S Unicast",
        "50P50S Multicast",
        "75P75S Unicast",
        "75P75S Multicast"
    ])
    
def ucast_vs_mcast_latency_line_plots():
    # ---------------------------------------------------------------------------- #
    #                                File Gathering                                #
    # ---------------------------------------------------------------------------- #
    lats = [file for file in get_files("data/v2/set_2") if "average_latencies" in file]
    ucast_lats = {
        "10p10s": [file for file in lats if "10p_10s" in file and "unicast" in file],
        "25p25s": [file for file in lats if "25p_25s" in file and "unicast" in file],
        "50p50s": [file for file in lats if "50p_50s" in file and "unicast" in file],
        "75p75s": [file for file in lats if "75p_75s" in file and "unicast" in file]
    }
    mcast_lats = {
        "10p10s": [file for file in lats if "10p_10s" in file and "multicast" in file],
        "25p25s": [file for file in lats if "25p_25s" in file and "multicast" in file],
        "50p50s": [file for file in lats if "50p_50s" in file and "multicast" in file],
        "75p75s": [file for file in lats if "75p_75s" in file and "multicast" in file]
    }

    # ---------------------------------------------------------------------------- #
    #                                  Data Frames                                 #
    # ---------------------------------------------------------------------------- #
    ucast_dfs = {}
    mcast_dfs = {}
    for item in ucast_lats:
        ucast_dfs[item] = (remove_infs_nans(pd.read_csv(ucast_lats[item][0])["run_1_latency"]) / 1000).to_frame('latency')['latency']
        mcast_dfs[item] = (remove_infs_nans(pd.read_csv(mcast_lats[item][0])["run_1_latency"]) / 1000).to_frame('latency')['latency']
    
    combined = {
        "u10p10s": ucast_dfs["10p10s"],
        "m10p10s": mcast_dfs["10p10s"],
        "u25p25s": ucast_dfs["25p25s"],
        "m25p25s": mcast_dfs["25p25s"],
        "u50p50s": ucast_dfs["50p50s"],
        "m50p50s": mcast_dfs["50p50s"],
        "u75p75s": ucast_dfs["75p75s"],
        "m75p75s": mcast_dfs["75p75s"]
    }
    
    # ---------------------------------------------------------------------------- #
    #                                    Figure                                    #
    # ---------------------------------------------------------------------------- #
    fig = plt.figure(figsize=(30, 30))
    
    # ---------------------------------------------------------------------------- #
    #                                     Grid                                     #
    # ---------------------------------------------------------------------------- #
    grid = plt.GridSpec(4, 4, figure=fig)
    
    row0 = plt.subplot(grid[0, 0:4])
    row1 = plt.subplot(grid[1, 0:4])
    row2 = plt.subplot(grid[2, 0:4])
    row3 = plt.subplot(grid[3, 0:4])
    
    # ---------------------------------------------------------------------------- #
    #                                  Line Plots                                  #
    # ---------------------------------------------------------------------------- #
    for item in ucast_dfs:
        if "10p10s" in item:
            title = "10P + 10S Unicast vs Multicast Latency Line Plot"
            ax = row0
        elif "25p25s" in item:
            title = "25P + 25S Unicast vs Multicast Latency Line Plot"
            ax = row1
        elif "50p50s" in item:
            title = "50P + 50S Unicast vs Multicast Latency Line Plot"
            ax = row2
        elif "75p75s" in item:
            title = "75P + 75S Unicast vs Multicast Latency Line Plot"
            ax = row3
        u_mean = ucast_dfs[item].mean()
        m_mean = mcast_dfs[item].mean()
        ax.plot(ucast_dfs[item], color=greens[0], label="Unicast")
        ax.plot(mcast_dfs[item], color=reds[0], label="Multicast")
        ax.set_yscale("log")
        ax.set_title(title, fontsize=15, fontweight="bold")
        ax.set_ylabel("Latency (ms)")
        ax.set_xlabel("Measurements Over Increasing Time")
        ax.legend()
        if ax != row3:
            ax.text(0.05 * ucast_dfs[item].shape[0], u_mean, "mean: " + str(format_number(u_mean)) + "ms", color=greens[0], backgroundcolor="#fff", fontsize=12)
            ax.axhline(u_mean, xmin=0, xmax=1, ls="--", color="#fff")
            
            ax.text(0.15 * mcast_dfs[item].shape[0], m_mean, "mean: " + str(format_number(m_mean)) + "ms", color=reds[0], backgroundcolor="#fff", fontsize=12)
            ax.axhline(m_mean, xmin=0, xmax=1, ls="--", color="#fff")
        else:
            ax.text(0.05 * ucast_dfs[item].shape[0], u_mean, "mean: " + str(format_number(u_mean)) + "ms", color=greens[0], backgroundcolor="#fff", fontsize=12)
            ax.axhline(u_mean, xmin=0, xmax=1, ls="--", color=greens[0])
            
            ax.text(0.15 * mcast_dfs[item].shape[0], m_mean, "mean: " + str(format_number(m_mean)) + "ms", color=reds[0], backgroundcolor="#fff", fontsize=12)
            ax.axhline(m_mean, xmin=0, xmax=1, ls="--", color=reds[0])
        
    row0.set_xlim(xmin=0, xmax=90000)
    row1.set_xlim(xmin=0, xmax=10000)
    row2.set_xlim(xmin=0, xmax=2500)
    row3.set_xlim(xmin=0, xmax=1000)
    
    plt.tight_layout()
    
def ucast_vs_mcast_cdfs():
    # ---------------------------------------------------------------------------- #
    #                                File Gathering                                #
    # ---------------------------------------------------------------------------- #
    lats = [file for file in get_files("data/v2/set_2") if "average_latencies" in file]
    ucast_lats = {
        "10p10s": [file for file in lats if "10p_10s" in file and "unicast" in file],
        "25p25s": [file for file in lats if "25p_25s" in file and "unicast" in file],
        "50p50s": [file for file in lats if "50p_50s" in file and "unicast" in file],
        "75p75s": [file for file in lats if "75p_75s" in file and "unicast" in file]
    }
    mcast_lats = {
        "10p10s": [file for file in lats if "10p_10s" in file and "multicast" in file],
        "25p25s": [file for file in lats if "25p_25s" in file and "multicast" in file],
        "50p50s": [file for file in lats if "50p_50s" in file and "multicast" in file],
        "75p75s": [file for file in lats if "75p_75s" in file and "multicast" in file]
    }

    # ---------------------------------------------------------------------------- #
    #                                  Data Frames                                 #
    # ---------------------------------------------------------------------------- #
    ucast_dfs = {}
    mcast_dfs = {}
    for item in ucast_lats:
        ucast_dfs[item] = (remove_infs_nans(pd.read_csv(ucast_lats[item][0])["run_1_latency"]) / 1000).to_frame('latency')['latency']
        mcast_dfs[item] = (remove_infs_nans(pd.read_csv(mcast_lats[item][0])["run_1_latency"]) / 1000).to_frame('latency')['latency']
    
    combined = {
        "u10p10s": ucast_dfs["10p10s"],
        "m10p10s": mcast_dfs["10p10s"],
        "u25p25s": ucast_dfs["25p25s"],
        "m25p25s": mcast_dfs["25p25s"],
        "u50p50s": ucast_dfs["50p50s"],
        "m50p50s": mcast_dfs["50p50s"],
        "u75p75s": ucast_dfs["75p75s"],
        "m75p75s": mcast_dfs["75p75s"]
    }
    
    # ---------------------------------------------------------------------------- #
    #                                    Figure                                    #
    # ---------------------------------------------------------------------------- #
    fig = plt.figure(figsize=(30, 20))
    
    # ---------------------------------------------------------------------------- #
    #                                     Grid                                     #
    # ---------------------------------------------------------------------------- #
    grid = plt.GridSpec(4, 4, figure=fig)
    
    top0 = plt.subplot(grid[0, 0])
    top1 = plt.subplot(grid[0, 1])
    top2 = plt.subplot(grid[0, 2])
    top3 = plt.subplot(grid[0, 3])
    
    main = plt.subplot(grid[1:4, 0:4])
    
    # ---------------------------------------------------------------------------- #
    #                                     CDFs                                     #
    # ---------------------------------------------------------------------------- #
    for item in ucast_dfs:
        if "10" in item:
            ax = top0
            title = "10P + 10S Unicast vs Multicast Latency CDF"
        elif "25" in item:
            ax = top1
            title = "25P + 25S Unicast vs Multicast Latency CDF"
        elif "50" in item:
            ax = top2
            title = "50P + 50S Unicast vs Multicast Latency CDF"
        elif "75" in item:
            ax = top3
            title = "75P + 75S Unicast vs Multicast Latency CDF"
        ax.set_title(title, fontsize=12, fontweight="bold")
        plot_cdf("Unicast", ucast_dfs[item], ax, greens[0], 'normal')
        plot_cdf("Multicast", mcast_dfs[item], ax, reds[0], 'normal')
        plot_cdf(item + " Unicast", ucast_dfs[item], main, greens[0], 'normal')
        plot_cdf(item + " Multicast", mcast_dfs[item], main, reds[0], 'normal')
        ax.legend()
        ax.grid(color="#ddd")
        ax.set_ylim(ymin=0, ymax=1)
        ax.set_ylabel("$F(x)$")
        ax.set_xlabel("Latency (ms)")
    # ---------------------------------------------------------------------------- #
    #                                   X-Limits                                   #
    # ---------------------------------------------------------------------------- #
    top0.set_xlim(xmin=0, xmax=13)
    top1.set_xlim(xmin=0, xmax=100)
    top2.set_xlim(xmin=0, xmax=500)
    top3.set_xlim(xmin=0, xmax=1250)
    
    # ---------------------------------------------------------------------------- #
    #                                 Main Settings                                #
    # ---------------------------------------------------------------------------- #
    main.set_ylabel("$F(x)$")
    main.set_xlabel("Latency (ms)")
    main.set_ylim(ymin=-0.02, ymax=1.02)
    main.set_xlim(xmin=0, xmax=1000)
    main.grid(color="#ddd")
    labelLines(main.get_lines(), align=False)
    
def ucast_vs_mcast_tp_boxplots():
    # ---------------------------------------------------------------------------- #
    #                                File Gathering                                #
    # ---------------------------------------------------------------------------- #
    tps = [file for file in get_files("data/v2/set_2") if "average_throughput" in file]
    ucast_tps = {
        "10p10s": [file for file in tps if "10p_10s" in file and "unicast" in file],
        "25p25s": [file for file in tps if "25p_25s" in file and "unicast" in file],
        "50p50s": [file for file in tps if "50p_50s" in file and "unicast" in file],
        "75p75s": [file for file in tps if "75p_75s" in file and "unicast" in file]
    }
    mcast_tps = {
        "10p10s": [file for file in tps if "10p_10s" in file and "multicast" in file],
        "25p25s": [file for file in tps if "25p_25s" in file and "multicast" in file],
        "50p50s": [file for file in tps if "50p_50s" in file and "multicast" in file],
        "75p75s": [file for file in tps if "75p_75s" in file and "multicast" in file]
    }
    # ---------------------------------------------------------------------------- #
    #                                  Data Frames                                 #
    # ---------------------------------------------------------------------------- #
    ucast_tp_dfs = {}
    mcast_tp_dfs = {}
    for item in ucast_tps:
        ucast_tp_dfs[item] = remove_infs_nans(get_total_tp(ucast_tps[item])["run_1_throughput"])
        mcast_tp_dfs[item] = remove_infs_nans(get_total_tp(mcast_tps[item])["run_1_throughput"])
        
    combined = {
        "u10p10s": ucast_tp_dfs["10p10s"],
        "m10p10s": mcast_tp_dfs["10p10s"],
        "u25p25s": ucast_tp_dfs["25p25s"],
        "m25p25s": mcast_tp_dfs["25p25s"],
        "u50p50s": ucast_tp_dfs["50p50s"],
        "m50p50s": mcast_tp_dfs["50p50s"],
        "u75p75s": ucast_tp_dfs["75p75s"],
        "m75p75s": mcast_tp_dfs["75p75s"]
    }
    
    # ---------------------------------------------------------------------------- #
    #                                    Figure                                    #
    # ---------------------------------------------------------------------------- #
    # fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(30, 5))
    fig = plt.figure(figsize=(30, 20))
    fig.suptitle("Unicast vs Multicast for Varying Participants Throughput Boxplots", fontsize=15, fontweight="bold")
    
    # ---------------------------------------------------------------------------- #
    #                                     Grids                                    #
    # ---------------------------------------------------------------------------- #
    grid = plt.GridSpec(4, 4, figure=fig)
    
    top0 = plt.subplot(grid[0, 0])
    top1 = plt.subplot(grid[0, 1])
    top2 = plt.subplot(grid[0, 2])
    top3 = plt.subplot(grid[0, 3])
    
    main = plt.subplot(grid[1:4, 0:4])
    
    # ---------------------------------------------------------------------------- #
    #                                   Box Plots                                  #
    # ---------------------------------------------------------------------------- #
    for item in ucast_tp_dfs:
        if "10p10s" in item:
            title = "10P + 10S Unicast vs Multicast Throughput Boxplots"
            ax = top0
        elif "25p25s" in item:
            title = "25P + 25S Unicast vs Multicast Throughput Boxplots"
            ax = top1
        elif "50p50s" in item:
            title = "50P + 50S Unicast vs Multicast Throughput Boxplots"
            ax = top2
        elif "75p75s" in item:
            title = "75P + 75S Unicast vs Multicast Throughput Boxplots"
            ax = top3
            
        new_dict = {"ucast": ucast_tp_dfs[item], "mcast": mcast_tp_dfs[item]}
        box = ax.boxplot(new_dict.values(), showfliers=False, patch_artist=True)
        
        colors = [greens[0], reds[0], greens[0], reds[0], greens[0], reds[0], greens[0], reds[0]]
        for patch, color in zip(box['boxes'], colors):
            patch.set_facecolor(color)

        ax.set_xticklabels(["Unicast", "Multicast"])
        ax.set_title(title)
        ax.grid(axis="y", color="#ddd")
        ax.spines.right.set_visible(False)
        ax.spines.top.set_visible(False)
        ax.spines.bottom.set_color("#999")
        ax.spines.left.set_color("#999")
        ax.set_ylabel("Throughput (mbps)")
        # ax.set_ylim(ymin=0)
        
    main_box = main.boxplot(combined.values(), showfliers=False, patch_artist=True)
    for patch, color in zip(main_box['boxes'], colors):
            patch.set_facecolor(color)
    # main.set_yscale("log")
    main.spines.top.set_visible(False)
    main.spines.right.set_visible(False)
    main.spines.bottom.set_color("#999")
    main.spines.left.set_color("#999")
    main.set_ylabel("Throughput (mbps)")
    main.set_title("Combined Unicast vs Multicast Throughput Boxplots")
    main.grid(axis="y", color="#ddd")
    main.set_xticklabels([
        "10P10S Unicast",
        "10P10S Multicast",
        "25P25S Unicast",
        "25P25S Multicast",
        "50P50S Unicast",
        "50P50S Multicast",
        "75P75S Unicast",
        "75P75S Multicast"
    ])
    
def ucast_vs_mcast_tp_line_plots():
    # ---------------------------------------------------------------------------- #
    #                                File Gathering                                #
    # ---------------------------------------------------------------------------- #
    tps = [file for file in get_files("data/v2/set_2") if "average_throughput" in file]
    ucast_tps = {
        "10p10s": [file for file in tps if "10p_10s" in file and "unicast" in file],
        "25p25s": [file for file in tps if "25p_25s" in file and "unicast" in file],
        "50p50s": [file for file in tps if "50p_50s" in file and "unicast" in file],
        "75p75s": [file for file in tps if "75p_75s" in file and "unicast" in file]
    }
    mcast_tps = {
        "10p10s": [file for file in tps if "10p_10s" in file and "multicast" in file],
        "25p25s": [file for file in tps if "25p_25s" in file and "multicast" in file],
        "50p50s": [file for file in tps if "50p_50s" in file and "multicast" in file],
        "75p75s": [file for file in tps if "75p_75s" in file and "multicast" in file]
    }

    # ---------------------------------------------------------------------------- #
    #                                  Data Frames                                 #
    # ---------------------------------------------------------------------------- #
    ucast_dfs = {}
    mcast_dfs = {}
    for item in ucast_tps:
        ucast_dfs[item] = remove_infs_nans(get_total_tp(ucast_tps[item])["run_1_throughput"])
        mcast_dfs[item] = remove_infs_nans(get_total_tp(mcast_tps[item])["run_1_throughput"])
    
    combined = {
        "u10p10s": ucast_dfs["10p10s"],
        "m10p10s": mcast_dfs["10p10s"],
        "u25p25s": ucast_dfs["25p25s"],
        "m25p25s": mcast_dfs["25p25s"],
        "u50p50s": ucast_dfs["50p50s"],
        "m50p50s": mcast_dfs["50p50s"],
        "u75p75s": ucast_dfs["75p75s"],
        "m75p75s": mcast_dfs["75p75s"]
    }
    
    # ---------------------------------------------------------------------------- #
    #                                    Figure                                    #
    # ---------------------------------------------------------------------------- #
    fig = plt.figure(figsize=(30, 30))
    
    # ---------------------------------------------------------------------------- #
    #                                     Grid                                     #
    # ---------------------------------------------------------------------------- #
    grid = plt.GridSpec(4, 4, figure=fig)
    
    row0 = plt.subplot(grid[0, 0:4])
    row1 = plt.subplot(grid[1, 0:4])
    row2 = plt.subplot(grid[2, 0:4])
    row3 = plt.subplot(grid[3, 0:4])
    
    # ---------------------------------------------------------------------------- #
    #                                  Line Plots                                  #
    # ---------------------------------------------------------------------------- #
    for item in ucast_dfs:
        if "10p10s" in item:
            title = "10P + 10S Unicast vs Multicast Throughput Line Plot"
            ax = row0
        elif "25p25s" in item:
            title = "25P + 25S Unicast vs Multicast Throughput Line Plot"
            ax = row1
        elif "50p50s" in item:
            title = "50P + 50S Unicast vs Multicast Throughput Line Plot"
            ax = row2
        elif "75p75s" in item:
            title = "75P + 75S Unicast vs Multicast Throughput Line Plot"
            ax = row3
        u_mean = ucast_dfs[item].mean()
        m_mean = mcast_dfs[item].mean()
        ax.plot(ucast_dfs[item], color=greens[0], label="Unicast")
        ax.plot(mcast_dfs[item], color=reds[0], label="Multicast")
        # ax.set_yscale("log")
        ax.set_title(title, fontsize=15, fontweight="bold")
        ax.set_ylabel("Throughput (mbps)")
        ax.set_xlabel("Increasing Time (s)")
        ax.legend()
        
        ax.text(0.05 * ucast_dfs[item].shape[0], u_mean, "mean: " + str(format_number(u_mean)) + "mbps", color=greens[0], backgroundcolor="#fff", fontsize=12)
        ax.axhline(u_mean, xmin=0, xmax=1, ls="--", color="#fff")
        
        ax.text(0.15 * mcast_dfs[item].shape[0], m_mean, "mean: " + str(format_number(m_mean)) + "mbps", color=reds[0], backgroundcolor="#fff", fontsize=12)
        ax.axhline(m_mean, xmin=0, xmax=1, ls="--", color="#fff")
        
    row0.set_xlim(xmin=0, xmax=21600)
    row1.set_xlim(xmin=0, xmax=21600)
    row2.set_xlim(xmin=0, xmax=21600)
    row3.set_xlim(xmin=0, xmax=21600)
    
    plt.tight_layout()
    
def ucast_vs_mcast_tp_cdfs():
    # ---------------------------------------------------------------------------- #
    #                                File Gathering                                #
    # ---------------------------------------------------------------------------- #
    tps = [file for file in get_files("data/v2/set_2") if "average_throughput" in file]
    ucast_tps = {
        "10p10s": [file for file in tps if "10p_10s" in file and "unicast" in file],
        "25p25s": [file for file in tps if "25p_25s" in file and "unicast" in file],
        "50p50s": [file for file in tps if "50p_50s" in file and "unicast" in file],
        "75p75s": [file for file in tps if "75p_75s" in file and "unicast" in file]
    }
    mcast_tps = {
        "10p10s": [file for file in tps if "10p_10s" in file and "multicast" in file],
        "25p25s": [file for file in tps if "25p_25s" in file and "multicast" in file],
        "50p50s": [file for file in tps if "50p_50s" in file and "multicast" in file],
        "75p75s": [file for file in tps if "75p_75s" in file and "multicast" in file]
    }

    # ---------------------------------------------------------------------------- #
    #                                  Data Frames                                 #
    # ---------------------------------------------------------------------------- #
    ucast_dfs = {}
    mcast_dfs = {}
    for item in ucast_tps:
        ucast_dfs[item] = remove_infs_nans(get_total_tp(ucast_tps[item])["run_1_throughput"])
        mcast_dfs[item] = remove_infs_nans(get_total_tp(mcast_tps[item])["run_1_throughput"])
    
    combined = {
        "u10p10s": ucast_dfs["10p10s"],
        "m10p10s": mcast_dfs["10p10s"],
        "u25p25s": ucast_dfs["25p25s"],
        "m25p25s": mcast_dfs["25p25s"],
        "u50p50s": ucast_dfs["50p50s"],
        "m50p50s": mcast_dfs["50p50s"],
        "u75p75s": ucast_dfs["75p75s"],
        "m75p75s": mcast_dfs["75p75s"]
    }
    
    # ---------------------------------------------------------------------------- #
    #                                    Figure                                    #
    # ---------------------------------------------------------------------------- #
    fig = plt.figure(figsize=(30, 20))
    
    # ---------------------------------------------------------------------------- #
    #                                     Grid                                     #
    # ---------------------------------------------------------------------------- #
    grid = plt.GridSpec(4, 4, figure=fig)
    
    top0 = plt.subplot(grid[0, 0])
    top1 = plt.subplot(grid[0, 1])
    top2 = plt.subplot(grid[0, 2])
    top3 = plt.subplot(grid[0, 3])
    
    main = plt.subplot(grid[1:4, 0:4])
    
    # ---------------------------------------------------------------------------- #
    #                                     CDFs                                     #
    # ---------------------------------------------------------------------------- #
    for item in ucast_dfs:
        if "10" in item:
            ax = top0
            title = "10P + 10S Unicast vs Multicast Throughput CDF"
        elif "25" in item:
            ax = top1
            title = "25P + 25S Unicast vs Multicast Throughput CDF"
        elif "50" in item:
            ax = top2
            title = "50P + 50S Unicast vs Multicast Throughput CDF"
        elif "75" in item:
            ax = top3
            title = "75P + 75S Unicast vs Multicast Throughput CDF"
        ax.set_title(title, fontsize=12, fontweight="bold")
        plot_cdf("Unicast", ucast_dfs[item], ax, greens[0], 'normal')
        plot_cdf("Multicast", mcast_dfs[item], ax, reds[0], 'normal')
        plot_cdf(item + " Unicast", ucast_dfs[item], main, greens[0], 'normal')
        plot_cdf(item + " Multicast", mcast_dfs[item], main, reds[0], 'normal')
        ax.legend()
        ax.grid(color="#ddd")
        ax.set_ylim(ymin=0, ymax=1)
        ax.set_ylabel("$F(x)$")
        ax.set_xlabel("Throughput (mbps)")
        ax.spines.top.set_visible(False)
        ax.spines.right.set_visible(False)
    # ---------------------------------------------------------------------------- #
    #                                   X-Limits                                   #
    # ---------------------------------------------------------------------------- #
    top0.set_xlim(xmin=200, xmax=350)
    top1.set_xlim(xmin=125, xmax=250)
    top2.set_xlim(xmin=100, xmax=200)
    top3.set_xlim(xmin=100, xmax=200)
    
    # ---------------------------------------------------------------------------- #
    #                                 Main Settings                                #
    # ---------------------------------------------------------------------------- #
    main.set_ylabel("$F(x)$")
    main.set_xlabel("Throughput (mbps)")
    main.set_ylim(ymin=-0.02, ymax=1.02)
    main.set_xlim(xmin=100, xmax=350)
    main.grid(color="#ddd")
    main.spines.top.set_visible(False)
    main.spines.right.set_visible(False)
    labelLines(main.get_lines(), align=False)