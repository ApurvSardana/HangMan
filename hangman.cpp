#include <bits/stdc++.h>
using namespace std;

class Game
{
    vector<string> items;

    public:
        string name;
        string answer;
        int turns = 5;

        Game()
        {
            ifstream readList("list.txt");
            while(getline(readList, name))
            {
                items.push_back(name);
            }
            name = "";
            selectItem();
        }

        void selectItem()
        {
            int index = rand() % (items.size() - 1);
            name = items[index];

            for(char ch : name)
            {
                if(ch != ' ')
                    answer += '_';
                else
                    answer += ' ';
            }

            displayAnswer();        
        }

        void inputCharacter()
        {
            char ch;
            cin >> ch;

            bool flag = false;
            for(int i = 0; i < name.length(); i++)
            {
                if(name[i] == ch || name[i] == ch - 32)
                {
                    flag = true;
                    turns = 5;
                    answer[i] = name[i];
                }
            }

            displayAnswer();

            if(!flag) turns--;
        }        

        void displayAnswer()
        {
            cout << "\t\t\t";
            for(char ch : answer)
                cout << ch << " ";
            
            cout << "\n";
        }

};

int main()
{
    cout << "\n\t\t\tWELCOME TO HANGMAN!!\n\t\tGUESS THE COUNTRY, ONE CHARACTER AT A TIME\n\t\t   YOU GET 5 CHANCES FOR EACH CHARACTER\n\n";
    int play;

    cout << "\t\t\tPRESS 1 TO PLAY\n";
    cin >> play;

    while(play == 1)
    {
        srand(time(0));
        Game g;

        while(g.turns > 0 && g.answer != g.name)
        {
            cout << "\n\t\t\tTurns : " << g.turns << "\n";
            g.inputCharacter();
        }

        if(g.answer == g.name)
            cout << "\n\t\t\tWIN\n";
        
        else
        {
            cout << "\n\t\t\tLOSS\n";
            cout << "\t\tTHE COUNTRY WAS : " << g.name;
        }

        cout << "\n\n\t\t\tPRESS 1 TO PLAY AGAIN\n";
        cin >> play;
    }

    return 0;
}