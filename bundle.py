import json
from utils import is_key


class Bundle(object):

    def __init__(self, json_bundle):
        # Load an instance of the bundle
        self._bundle = json.loads(json_bundle['content'])

    def get_test_results(self, id=None):
        test_runs = self.test_runs
        validated_results = []
        if test_runs:
            for test_results in test_runs:
                # Check for a valid result
                if is_key('test_id', test_results):
                    if id:
                        if id in test_results['test_id']:
                            return test_results
                    else:
                        validated_results.append(test_results)
            if len(validated_results) > 0:
                return validated_results

    @property
    def test_runs(self):
        if is_key('test_runs', self._bundle):
            # Get the boot data from LAVA
            return self._bundle['test_runs']

    @property
    def bundle_attributes(self):
        if is_key('attributes', self.test_runs[-1]):
            return self._bundle['test_runs'][-1]['attributes']


class KernelCIBundle(Bundle):

    def get_boot_metadata(self):
        boot_meta = {}
        boot_meta['version'] = '1.0'
        result = self.get_test_results(id='lava')
        if result:
            for test in result['test_results']:
                if test['test_case_id'] == 'test_kernel_boot_time':
                    boot_meta['boot_time'] = test['measurement']
                    break
            bundle_attributes = self.bundle_attributes
            if is_key('target', bundle_attributes):
                boot_meta['board_instance'] = bundle_attributes['target']
            if is_key('kernel.defconfig', bundle_attributes):
                kernel_defconfig = bundle_attributes['kernel.defconfig']
                boot_meta['arch'], kernel_defconfig_full = kernel_defconfig.split('-')
                kernel_defconfig_base = ''.join(kernel_defconfig_full.split('+')[:1])
                if kernel_defconfig_full == kernel_defconfig_base:
                    kernel_defconfig_full = None
                boot_meta['defconfig'] = kernel_defconfig_base
                if kernel_defconfig_full is not None:
                    boot_meta['defconfig_full'] = kernel_defconfig_full
                if is_key('kernel.version', bundle_attributes):
                    boot_meta['kernel'] = bundle_attributes['kernel.version']
                if is_key('device.tree', bundle_attributes):
                    device_tree = bundle_attributes['device.tree']
                    if device_tree:
                        boot_meta['dtb'] = 'dtbs/' + device_tree
                    else:
                        boot_meta['dtb'] = device_tree
                if is_key('kernel.endian', bundle_attributes):
                    boot_meta['endian'] = bundle_attributes['kernel.endian']
                if is_key('platform.fastboot', bundle_attributes):
                    boot_meta['fastboot'] = bundle_attributes['platform.fastboot']
                if is_key('kernel.tree', bundle_attributes):
                    boot_meta['job'] = bundle_attributes['kernel.tree']
                if is_key('kernel-image', bundle_attributes):
                    boot_meta['kernel_image'] = bundle_attributes['kernel-image']
                if is_key('kernel-addr', bundle_attributes):
                    boot_meta['loadaddr'] = bundle_attributes['kernel-addr']
                if is_key('initrd-addr', bundle_attributes):
                    boot_meta['initrd_addr'] = bundle_attributes['initrd-addr']
                if is_key('dtb-addr', bundle_attributes):
                    boot_meta['dtb_addr'] = bundle_attributes['dtb-addr']
                if is_key('dtb-append', bundle_attributes):
                    boot_meta['dtb_append'] = bundle_attributes['dtb-append']
                if is_key('boot_retries', bundle_attributes):
                     boot_meta['retries'] = int(bundle_attributes['boot_retries'])
            return boot_meta
