import os.path
import lettuce
import lettuce.fs

from ostack_validator.common import Inspection, Rule, Issue


class LettuceRunnerInspection(Inspection):
    base_path = os.path.join(os.path.dirname(__file__), 'lettuce')

    @classmethod
    def rules(klass):
        rules = []

        loader = lettuce.fs.FeatureLoader(klass.base_path)
        for path in loader.find_feature_files():
            feature = lettuce.Feature.from_file(path)
            for scenario in feature.scenarios:
                rules.append(Rule(scenario.name,
                                  "\n".join(scenario.remaining_lines)))
        return rules

    def inspect(self, openstack):
        runner = lettuce.Runner(base_path=self.base_path)

        lettuce.world.openstack = openstack
        result = runner.run()
        del lettuce.world.openstack

        for feature_result in result.feature_results:
            for scenario_result in feature_result.scenario_results:
                if scenario_result.passed:
                    continue

                for step in scenario_result.steps_undefined:
                    openstack.report_issue(
                        Issue(Issue.ERROR, 'Undefined step "%s"' %
                              step.sentence))
