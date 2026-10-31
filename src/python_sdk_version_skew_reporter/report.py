from .aggregation import VersionSkewAggregator

class TerminalReporter:
    """
    Displays a summary report of version skew findings in the terminal.
    Consumes a VersionSkewAggregator instance and prints the formatted summary.
    """
    def __init__(self, aggregator: VersionSkewAggregator):
        self.aggregator = aggregator

    def display(self) -> None:
        """
        Prints the formatted version skew summary to the terminal.
        """
        summary = self.aggregator.format_skew_summary()
        print(summary)

# Example usage (for integration, not executed here):
# aggregator = VersionSkewAggregator(skewed_packages, skew_details)
# reporter = TerminalReporter(aggregator)
# reporter.display()
