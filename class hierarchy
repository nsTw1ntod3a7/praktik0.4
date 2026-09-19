#include <iostream>
#include <string>
#include <windows.h>


// базовый класс Animal (Животное)
class Animal {
protected:
    std::string name;
    int age;

public:
    Animal(const std::string& name, int age) : name(name), age(age) {}

    // заглушки
   
    void Eat() {
    }

    void Sleep() {
    }
};

// наследуемые классы от Animal

class Bird : public Animal {
public:
    Bird(const std::string& name, int age) : Animal(name, age) {}

    void Fly() {
    }
};

class Fish : public Animal {
public:
    Fish(const std::string& name, int age) : Animal(name, age) {}

    void Swim() {
    }
};

class Mammal : public Animal {
public:
    Mammal(const std::string& name, int age) : Animal(name, age) {}

    void Walk() {
    }
};

int main() {
    SetConsoleOutputCP(65001);
    SetConsoleCP(65001);

    Bird bird("Попугай", 2);
    Fish fish("Золотая рыбка", 1);
    Mammal mammal("Лев", 5);

	// унаследованые и собственные методы классов
    bird.Eat();
    bird.Sleep();
    bird.Fly();

    fish.Eat();
    fish.Sleep();
    fish.Swim();

    mammal.Eat();
    mammal.Sleep();
    mammal.Walk();

    std::cout << "Иерархия классов Animal -> Bird/Fish/Mammal" << std::endl;

    return 0;
}
