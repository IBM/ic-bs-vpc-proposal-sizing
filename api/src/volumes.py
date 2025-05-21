from abc import ABC, abstractmethod
import math


class AbstractVolume(ABC):
    """
    thoughput: GB/s
    iops
    size: TB
    """

    @abstractmethod
    def get(self, thoughput: float, iops: int, size: int):
        pass

    """
    Return max size in TB's in the tier
    """

    @abstractmethod
    def max_size(self):
        pass

    """
    Return IOPS in the tier
    """

    @abstractmethod
    def max_iops(self):
        pass

    """
    Return Throughput in the tier
    """

    @abstractmethod
    def max_throughput(self):
        pass

    """
    Return Block size in the tier
    """

    @abstractmethod
    def default_block_size(self):
        pass

    def get(self, thoughput, iops, size):
        avg_block_size = thoughput * 1000 * 1000 / iops
        iops_per_disk = min(self.max_throughput(), self._max_bandwidth_from_bs_avg(size, avg_block_size)) / avg_block_size
        num_disk_iops = math.ceil(iops / iops_per_disk)
        num_disk_size = math.ceil(size / self.max_size())
        num_disk = max(num_disk_size, num_disk_iops)
        return {"case1": self._rebalance(size, thoughput, num_disk, avg_block_size),
                "case2": self._default_volumes(size, num_disk, iops_per_disk),
                "bs": self.default_block_size()}

    def _default_volumes(self, size, num_disks, iops_per_disk):
        size_per_disk = size / num_disks
        return [{"size": size_per_disk,
                 "iops_BS_AVG": iops_per_disk,
                 "iops_16KB": self.max_iops(),
                 "throughput": self.max_throughput() / 1000 / 1000}
                for i in range(num_disks)]

    def _rebalance(self, size, thoughput, num_disks, avg_block_size):
        size_per_disk = size / num_disks
        thoughput_per_disk = thoughput / num_disks
        iops_per_disk_16KB = math.ceil(float(thoughput_per_disk * 1000 * 1000) / (self.default_block_size() * 1.024))
        iops_per_disk_BS_AVG = math.ceil(thoughput_per_disk * 1000 * 1000 / avg_block_size)
        if(iops_per_disk_BS_AVG > iops_per_disk_16KB):
            iops_per_disk_16KB = max(iops_per_disk_16KB, iops_per_disk_BS_AVG)
            thoughput_per_disk = self._thoughput_at_defaut_bs(iops_per_disk_16KB)
        return [{"size": size_per_disk,
                 "iops_BS_AVG": iops_per_disk_BS_AVG,
                 "iops_16KB":iops_per_disk_16KB,
                 "throughput": thoughput_per_disk}
                for i in range(num_disks)]
    
    def _thoughput_at_defaut_bs(self, iops):
        return min(self.max_throughput(), iops * self.default_block_size()) / 1000 / 1000


class CustomVolume(AbstractVolume):

    def max_size(self):
        return 16

    def max_iops(self):
        return 48000

    def max_throughput(self):
        return 1000 * 1000

    def default_block_size(self):
        return 256
    
    def _max_bandwidth_from_bs_avg(self, size, avg_block_size):
        return self.max_iops() * avg_block_size
    

class TierVolume(AbstractVolume):

    """Must return 3, 5, 10"""
    @abstractmethod
    def tier(self):
        pass
    
    def _max_bandwidth_from_bs_avg(self, size, avg_block_size):
        return self.max_iops() * avg_block_size
    
    def _default_volumes(self, size, num_disks, iops_per_disk):
        return [{"size": self.max_size(),
                 "iops_BS_AVG": iops_per_disk,
                 "iops_16KB": self.max_iops(),
                 "throughput": self.max_throughput() / 1000 / 1000}
                for i in range(num_disks)]

    def _rebalance(self, size, thoughput, num_disks, avg_block_size):
        thoughput_per_disk = thoughput / num_disks
        iops_per_disk_BS_AVG = math.ceil(thoughput_per_disk * 1000 * 1000 / avg_block_size)
        iops_per_disk_16KB = math.ceil(float(thoughput_per_disk * 1000 * 1000) / (self.default_block_size() * 1.024))
        size_per_disk = math.ceil(iops_per_disk_16KB / self.tier())

        if(size_per_disk * num_disks < size * 1000):
            return self._rebalance_taking_account_size(size, thoughput, num_disks, avg_block_size)
        
        if(iops_per_disk_BS_AVG > iops_per_disk_16KB):
            iops_per_disk_16KB = max(iops_per_disk_16KB, iops_per_disk_BS_AVG)
            thoughput_per_disk = self._thoughput_at_defaut_bs(iops_per_disk_16KB)
            size_per_disk = iops_per_disk_16KB / self.tier()

        return [{"size": size_per_disk / 1000,
                 "iops_BS_AVG": iops_per_disk_BS_AVG,
                 "iops_16KB": iops_per_disk_16KB,
                 "throughput": thoughput_per_disk}
                for i in range(num_disks)]
    
    def _rebalance_taking_account_size(self, size, thoughput, num_disks, avg_block_size):
        size_per_disk = math.ceil(size / num_disks * 1000)
        iops_per_disk_16KB = size_per_disk * self.tier()
        thoughput_per_disk = min(self.max_throughput(), iops_per_disk_16KB * self.default_block_size() * 1.024) / 1000 / 1000
        iops_per_disk_BS_AVG = min(self.max_iops(), iops_per_disk_16KB * (self.default_block_size() * 1.024) / avg_block_size)

        if(iops_per_disk_BS_AVG > iops_per_disk_16KB):
            iops_per_disk_16KB = max(iops_per_disk_16KB, iops_per_disk_BS_AVG)
            thoughput_per_disk = self._thoughput_at_defaut_bs(iops_per_disk_16KB)
            size_per_disk = (iops_per_disk_16KB / self.tier())

        return [{"size": size_per_disk / 1000,
                 "iops_BS_AVG": iops_per_disk_BS_AVG,
                 "iops_16KB": iops_per_disk_16KB,
                 "throughput": thoughput_per_disk}
                for i in range(num_disks)]
    

class Tier3Volume(TierVolume):

    def max_size(self):
        return 16

    def max_iops(self):
        return 48000

    def max_throughput(self):
        return 1000 * 670

    def default_block_size(self):
        return 16
    
    def tier(self):
        return 3


class Tier5Volume(TierVolume):

    def max_size(self):
        return 9.6

    def max_iops(self):
        return 48000

    def max_throughput(self):
        return 1000 * 768

    def default_block_size(self):
        return 16
    
    def tier(self):
        return 5
    

class Tier10Volume(TierVolume):

    def max_size(self):
        return 4.8

    def max_iops(self):
        return 48000

    def max_throughput(self):
        return 1000 * 1000

    def default_block_size(self):
        return 256
    
    def tier(self):
        return 10


def volume(tier: str) -> AbstractVolume:
    if tier not in TIERS:
        raise Exception('Tier does not exists')
    return TIERS[tier]


TIERS = {
    'custom': CustomVolume(),
    'tier3': Tier3Volume(),
    'tier5': Tier5Volume(),
    'tier10': Tier10Volume(),
}