import sys
def main():
    data=open(sys.argv[1]).read().split()
    n=int(data[0]) if data else 0
    # the doc's checker convention: input file contains n
    n=int(open(sys.argv[1]).read().split()[0])
    out=list(map(int,open(sys.argv[2]).read().split()))
    if len(out)!=n:
        print('FAIL length'); sys.exit(1)
    if sorted(out)!=list(range(1,n+1)):
        print('FAIL not permutation'); sys.exit(1)
    diffs=[abs(out[i]-out[i+1]) for i in range(n-1)]
    if len(set(diffs))!=len(diffs):
        print('FAIL repeated difference'); sys.exit(1)
    print('OK')
main()
