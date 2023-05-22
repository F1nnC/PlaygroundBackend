#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>

// Define the structure for a user entry
struct User {
    int uid;
    std::string name;
    int score;
};

// Comparison function to sort users by score in descending order
bool compareByScore(const User& a, const User& b) {
    return a.score > b.score;
}

int main() {
    system("python supercoolfile.py");


    std::vector<User> users;



    std::sort(users.begin(), users.end(), compareByScore);


    for (const auto& user : users) {
        std::cout << "Name: " << user.name << ", Score: " << user.score << std::endl;
    }

    return 0;
}
