#include <iostream>
#include <vector>
#include <algorithm>
#include <fstream>


void sortUsernames(std::vector<std::string>& usernames) {
    std::sort(usernames.begin(), usernames.end());
}

int main() {

    std::vector<std::string> usernames;


    std::cout << "Enter usernames (type 'end' to finish):" << std::endl;
    std::string username;
    while (true) {
        std::cin >> username;
        if (username == "end") {
            break;
        }
        usernames.push_back(username);
    }


    sortUsernames(usernames);


    std::ofstream outputFile("sorted_usernames.txt");
    if (outputFile.is_open()) {
        for (const auto& name : usernames) {
            outputFile << name << std::endl;
        }
        outputFile.close();
        std::cout << "Sorted usernames saved to 'sorted_usernames.txt'." << std::endl;
    } else {
        std::cerr << "Unable to open file for writing!" << std::endl;
        return 1;
    }


    std::string pythonCommand = "python3 database_insertion.py sorted_usernames.txt";
    int result = system(pythonCommand.c_str());
    if (result != 0) {
        std::cerr << "An error occurred while executing the Python file." << std::endl;
        return 1;
    }

    return 0;
}
