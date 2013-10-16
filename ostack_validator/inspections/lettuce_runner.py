import os.path
import lettuce

from ostack_validator.common import Inspection, Issue


class LettuceRunnerInspection(Inspection):

    def inspect(self, openstack):
        runner = lettuce.Runner(
            base_path=os.path.join(os.path.dirname(__file__), 'lettuce')
        )

        lettuce.world.openstack = openstack
        result = runner.run()
        del lettuce.world.openstack

        for feature_result in result.feature_results:
            for scenario_result in [s for s in feature_result.scenario_results if not s.passed]:
                for step in scenario_result.steps_undefined:
                    openstack.report_issue(
                        Issue(
                            Issue.ERROR,
                            'Undefined step "%s"' %
                            step.sentence))
