r"""This module contains functions for visualizing data."""


def print_dataset(x_axis_dataset, y_axis_datasets, y_axis_datalabels,
                  x_axis_isdatetime=False,
                  title='Title', x_label='X-Label', y_label='Y-Label',
                  fontsize=8, fontweight='bold',
                  dateformat='%d.%m.%Y\n%H:%M', block=True):
    """Print the given dataset."""
    from matplotlib.dates import AutoDateLocator, DateFormatter
    import matplotlib.pyplot as plt

    if len(x_axis_dataset) <= 0:
        raise ValueError('Lists for X-axis is empty!')

    for y_axis_dataset in y_axis_datasets:
        if len(x_axis_dataset) != len(y_axis_dataset):
            raise ValueError(
                'Lists for X- and Y-axis with non-identical length!')

    plt.figure()
    plt.subplot(111)

    for i, y_axis_dataset in enumerate(y_axis_datasets):
        plt.plot(x_axis_dataset, y_axis_dataset, '-',
                 label=y_axis_datalabels[i])

    plt.grid(True)
    plt.xlabel(x_label, fontsize=fontsize, fontweight=fontweight)
    plt.ylabel(y_label, fontsize=fontsize, fontweight=fontweight)
    plt.title(title, fontsize=(fontsize + 2), fontweight=fontweight)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=5, borderaxespad=0.)

    if x_axis_isdatetime:
        locator = AutoDateLocator()
        formatter = DateFormatter(dateformat)
        plt.subplot(111).xaxis.set_major_locator(locator)
        plt.subplot(111).xaxis.set_major_formatter(formatter)

    plt.subplot(111).autoscale_view()
    plt.show(block)
