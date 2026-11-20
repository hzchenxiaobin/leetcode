# CF48F 浮点校验：相对/绝对误差 <= 1e-9
import sys
try:
    got = float(open(sys.argv[2]).read().split()[0])
    exp = float(open(sys.argv[3]).read().split()[0])
except Exception as e:
    print('parse error', e); sys.exit(1)
err = abs(got - exp)
if err <= 1e-9 or err <= 1e-9 * max(1.0, abs(exp)):
    sys.exit(0)
print('wrong answer: %.17g vs %.17g (err %.3e)' % (got, exp, err)); sys.exit(1)
