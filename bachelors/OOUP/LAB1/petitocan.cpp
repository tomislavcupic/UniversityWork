#include <iostream>

class B {
public:
    virtual int prva() = 0;
    virtual int druga(int) = 0;
};

class D : public B {
public:
    virtual int prva() { return 42; }
    virtual int druga(int x) { return prva() + x; }
};

typedef int (*PrvaFunkcija)(B*);
typedef int (*DrugaFunkcija)(B*, int);

void ispisiPovratneVrijednosti(B* pb) {
    PrvaFunkcija prva = reinterpret_cast<PrvaFunkcija>(*reinterpret_cast<void**>(pb));
    DrugaFunkcija druga = reinterpret_cast<DrugaFunkcija>(*reinterpret_cast<void**>(pb) + 1);

    std::cout << "Povratna vrijednost prva(): " << prva(pb) << std::endl;
    std::cout << "Povratna vrijednost druga(): " << druga(pb, 7) << std::endl;
}

int main() {
    std::cout << "test" << std::endl;
    D d;
    ispisiPovratneVrijednosti(&d);
    return 0;
}
