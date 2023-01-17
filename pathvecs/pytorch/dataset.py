import torch
from torch.utils.data import Sampler, Dataset, RandomSampler


class WordContextDataset(Dataset):
    """ Map-stype interface for a set of word-context pairs

    For every drawn sample pair, (N) additional contexts are randomly drawn as
    negative samples.
    """

    def __init__(self, pairs_data, negative_samples=5):
        super(WordContextDataset).__init__()

        self.pairs_data = pairs_data
        self.negative_samples = negative_samples
        self.negative_sampler = UnigramSampler(
            data_source=self.pairs_data[:,1],
            num_samples=negative_samples
        )

    def __getitem__(self, idx):
        w_pos = self.pairs_data[idx, 0]
        c_pos = self.pairs_data[idx, 1]
        c_neg = torch.as_tensor(list(iter(self.negative_sampler)))

        return w_pos, c_pos, c_neg

    def __len__(self):
        return len(self.pairs_data)


class UnigramSampler(Sampler):
    """ Draws samples from the unigram (word frequency) distribution

    This can be used for negative sampling. Using the table method from the
    original paper ended up being faster than pytorch's WeightedRandomSampler,
    probably with memory overhead cost which is fine at this scale
    """

    def __init__(
        self,
        data_source,
        num_samples=5,
        table_size=1e8,
        generator=None
    ):

        self.data_source = data_source
        self.table_size = table_size
        self.num_samples = num_samples

        self.generator = generator
        self._init_unigram_table(data_source)
        self.random_sampler = RandomSampler(
            self.unigram_table,
            num_samples=num_samples,
            generator=generator,
            replacement=True
        )

        super().__init__(self.data_source)

    def __iter__(self):
        for i in self.random_sampler:
            yield self.unigram_table[i]

    def __len__(self):
        return len(self.data_source)

    def _init_unigram_table(self, data):
        """ Initialize a unigram table to sample from given the observed data

        Create a large ( n >> len(vocab) ) vector of sample indices allocated
        proportional to the frequency of the observations raised to some power.
        pow = 0.75 is what was used in Mikolov et al.
        """

        freqs = torch.bincount(data)
        sample_ratios = freqs.pow(0.75)
        sample_ratios /= sample_ratios.sum()
        allotments = (sample_ratios * self.table_size).type(torch.int32)
        samples = [
            torch.full([num], i)
            for i, num in enumerate(allotments.data.tolist())
        ]
        self.unigram_table = torch.cat(samples)
