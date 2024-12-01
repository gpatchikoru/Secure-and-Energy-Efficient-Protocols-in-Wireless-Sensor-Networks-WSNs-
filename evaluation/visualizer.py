# evaluation/visualizer.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class Visualizer:
    def visualize_results(self, results):
        """
        Generate comparative plots for protocol performance.
        
        :param results: Dictionary containing protocol metrics
        """
        # Transform results into a DataFrame
        data = []
        for protocol, metrics in results.items():
            data.append({
                "Protocol": protocol,
                "Encryption Time (s)": metrics.get("Encryption Time (s)", 0),
                "Decryption Time (s)": metrics.get("Decryption Time (s)", 0),
                "Energy Consumption (J)": metrics.get("Energy Consumption (J)", 0),
                "Packet Size (bytes)": metrics.get("Packet Size (bytes)", 0),
                "Network Lifetime (cycles)": metrics.get("Network Lifetime (cycles)", 0)
            })

        df = pd.DataFrame(data)

        # Set Seaborn style
        sns.set(style="whitegrid", font_scale=1.2)

        # Plot Encryption Time
        plt.figure(figsize=(10, 6))
        sns.barplot(x="Protocol", y="Encryption Time (s)", data=df, hue="Protocol", dodge=False, palette="Blues_d")
        plt.title("Encryption Time by Protocol")
        plt.ylabel("Time (seconds)")
        plt.xlabel("Protocol")
        plt.xticks(rotation=45)
        plt.legend([], [], frameon=False)
        plt.tight_layout()
        plt.savefig("results/encryption_time.png")
        plt.show()

        # Plot Decryption Time
        plt.figure(figsize=(10, 6))
        sns.barplot(x="Protocol", y="Decryption Time (s)", data=df, hue="Protocol", dodge=False, palette="Greens_d")
        plt.title("Decryption Time by Protocol")
        plt.ylabel("Time (seconds)")
        plt.xlabel("Protocol")
        plt.xticks(rotation=45)
        plt.legend([], [], frameon=False)
        plt.tight_layout()
        plt.savefig("results/decryption_time.png")
        plt.show()

        # Plot Energy Consumption
        plt.figure(figsize=(10, 6))
        sns.barplot(x="Protocol", y="Energy Consumption (J)", data=df, hue="Protocol", dodge=False, palette="Reds_d")
        plt.title("Energy Consumption by Protocol")
        plt.ylabel("Energy (Joules)")
        plt.xlabel("Protocol")
        plt.xticks(rotation=45)
        plt.legend([], [], frameon=False)
        plt.tight_layout()
        plt.savefig("results/energy_consumption.png")
        plt.show()

        # Plot Packet Size
        plt.figure(figsize=(10, 6))
        sns.barplot(x="Protocol", y="Packet Size (bytes)", data=df, hue="Protocol", dodge=False, palette="Purples_d")
        plt.title("Packet Size by Protocol")
        plt.ylabel("Size (bytes)")
        plt.xlabel("Protocol")
        plt.xticks(rotation=45)
        plt.legend([], [], frameon=False)
        plt.tight_layout()
        plt.savefig("results/packet_size.png")
        plt.show()

        # Plot Network Lifetime
        plt.figure(figsize=(10, 6))
        sns.barplot(x="Protocol", y="Network Lifetime (cycles)", data=df, hue="Protocol", dodge=False, palette="Oranges_d")
        plt.title("Network Lifetime by Protocol")
        plt.ylabel("Lifetime (cycles)")
        plt.xlabel("Protocol")
        plt.xticks(rotation=45)
        plt.legend([], [], frameon=False)
        plt.tight_layout()
        plt.savefig("results/network_longevity.png")
        plt.show()

        # **New Addition: Scatter Plot for Energy vs. Encryption Time**
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x="Encryption Time (s)", y="Energy Consumption (J)", hue="Protocol", data=df, palette="deep", s=100)
        plt.title("Energy Consumption vs. Encryption Time")
        plt.xlabel("Encryption Time (seconds)")
        plt.ylabel("Energy Consumption (Joules)")
        plt.legend(title="Protocol", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig("results/energy_vs_encryption_time.png")
        plt.show()

        # **New Addition: Heatmap of Metrics**
        metrics_df = df.set_index("Protocol")
        plt.figure(figsize=(12, 8))
        sns.heatmap(metrics_df, annot=True, cmap="YlGnBu", fmt=".4g")
        plt.title("Heatmap of Protocol Metrics")
        plt.ylabel("Protocol")
        plt.xlabel("Metrics")
        plt.tight_layout()
        plt.savefig("results/metrics_heatmap.png")
        plt.show()
