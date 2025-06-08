#include <bits/stdc++.h>
using namespace std;

class Game {
    vector<string> items;
    string name, answer;
    int turns;
    bool gameRunning;

public:
    Game() {
        turns = 5;
        gameRunning = true;
        
        // Initialize files
        ofstream clearInput("input.txt", ofstream::trunc);
        clearInput.close();
        
        ofstream clearGameState("game_state.txt", ofstream::trunc);
        clearGameState.close();
        
        // Read word list
        ifstream readList("list.txt");
        if (!readList.is_open()) {
            cerr << "Error: Could not open list.txt" << endl;
            return;
        }
        
        string line;
        while (getline(readList, line)) {
            if (!line.empty()) {
                items.push_back(line);
            }
        }
        readList.close();
        
        if (items.empty()) {
            cerr << "Error: No words found in list.txt" << endl;
            return;
        }
        
        selectItem();
    }

    void selectItem() {
        srand(time(0));
        int index = rand() % items.size();
        name = items[index];

        answer = string(name.length(), '_');
        for (int i = 0; i < name.length(); i++) {
            if (name[i] == ' ') answer[i] = ' ';
        }

        updateGameState();
    }

    void inputCharacter(char ch) {
        if (!gameRunning) return;
        
        bool found = false;
        for (int i = 0; i < name.length(); i++) {
            if ((name[i] == ch || name[i] == ch - 32) && answer[i] != name[i]) {
                found = true;
                answer[i] = name[i];
            }
        }
        if (!found) turns--;

        updateGameState();
        
        if (isGameOver()) {
            gameRunning = false;
        }
    }

    void updateGameState() {
        ofstream outFile("game_state.txt");
        if (!outFile.is_open()) {
            cerr << "Error: Could not open game_state.txt" << endl;
            return;
        }
        outFile << name << "\n" << answer << "\n" << turns;
        outFile.close();
    }

    bool isGameOver() {
        return (turns == 0 || answer == name);
    }

    string getAnswer() { return answer; }
    string getName() { return name; }
    int getTurns() { return turns; }

    void playGame() {
        while (gameRunning) {
            char ch = '\0';
            ifstream inputFile("input.txt");
            if (inputFile.is_open()) {
                inputFile >> ch;
                inputFile.close();
                
                if (ch != '\0') {
                    // Clear the input file
                    ofstream clearInput("input.txt", ofstream::trunc);
                    clearInput.close();
                    
                    inputCharacter(ch);
                }
            }
            this_thread::sleep_for(chrono::milliseconds(100));
        }
    }
};

int main() {
    Game g;
    g.playGame();
    return 0;
}
