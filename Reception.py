#include <iostream>
#include <fstream>
#include <string>
#include <limits> // For std::numeric_limits

using namespace std;

struct Patient {
    string name;
    int age;
    string ailment;
    Patient* next; // Pointer to the next patient
};

class HospitalManagement {
private:
    Patient* head; // Head of the linked list
    string filename;

public:
    HospitalManagement(const string& file) : filename(file), head(nullptr) {
        loadFromFile(); // Load patients from file on initialization
    }

    ~HospitalManagement() {
        // Free the linked list memory
        while (head) {
            Patient* temp = head;
            head = head->next;
            delete temp;
        }
    }

    void addPatient(const Patient& patient) {
        Patient* newPatient = new Patient{patient.name, patient.age, patient.ailment, nullptr};
        if (!head) {
            head = newPatient; // If the list is empty, set the new patient as head
        } else {
            Patient* temp = head;
            while (temp->next) {
                temp = temp->next; // Traverse to the end of the list
            }
            temp->next = newPatient; // Add the new patient at the end
        }
        if (!saveToFile(patient)) {
            cerr << "Failed to save patient to file. Patient was not added." << endl;
        }
    }

    void displayPatients() {
        if (!head) {
            cout << "No patients in the list." << endl;
            return;
        }
        Patient* temp = head;
        while (temp) {
            cout << "Name: " << temp->name << ", Age: " << temp->age << ", Ailment: " << temp->ailment << endl;
            temp = temp->next;
        }
    }

    void modifyPatient(const string& name, const Patient& newDetails) {
        Patient* temp = head;
        while (temp) {
            if (temp->name == name) {
                temp->name = newDetails.name;
                temp->age = newDetails.age;
                temp->ailment = newDetails.ailment;
                saveAllToFile();
                cout << "Patient modified successfully." << endl;
                return;
            }
            temp = temp->next;
        }
        cout << "Patient not found." << endl;
    }

    void searchPatient(const string& name) {
        Patient* temp = head;
        while (temp) {
            if (temp->name == name) {
                cout << "Found: Name: " << temp->name << ", Age: " << temp->age << ", Ailment: " << temp->ailment << endl;
                return;
            }
            temp = temp->next;
        }
        cout << "Patient not found." << endl;
    }

    void deletePatient(const string& name) {
        Patient* temp = head;
        Patient* prev = nullptr;

        while (temp) {
            if (temp->name == name) {
                if (prev) {
                    prev->next = temp->next; // Bypass the patient to delete
                } else {
                    head = temp->next; // Move head if the first patient is deleted
                }
                delete temp; // Free memory
                saveAllToFile();
                cout << "Patient deleted." << endl;
                return;
            }
            prev = temp;
            temp = temp->next;
        }
        cout << "Patient not found." << endl;
    }

private:
    bool saveToFile(const Patient& patient) {
        ofstream outFile(filename, ios::app);
        if (!outFile) {
            cerr << "Error opening file for writing." << endl;
            return false;
        }
        outFile << patient.name << "," << patient.age << "," << patient.ailment << endl;
        outFile.close();
        return true;
    }

    void saveAllToFile() {
        ofstream outFile(filename);
        if (!outFile) {
            cerr << "Error opening file for writing." << endl;
            return;
        }
        Patient* temp = head;
        while (temp) {
            outFile << temp->name << "," << temp->age << "," << temp->ailment << endl;
            temp = temp->next;
        }
        outFile.close();
    }

    void loadFromFile() {
        ifstream inFile(filename);
        if (!inFile) return; // file doesn't exist exit the funtcion

        string line;
        while (getline(inFile, line)) {
            size_t pos1 = line.find(',');
            size_t pos2 = line.find(',', pos1 + 1);
            if (pos1 != string::npos && pos2 != string::npos) {
                Patient* newPatient = new Patient; // Allocate memory for a new patient
                newPatient->name = line.substr(0, pos1);
                newPatient->age = stoi(line.substr(pos1 + 1, pos2 - pos1 - 1));
                newPatient->ailment = line.substr(pos2 + 1);
                newPatient->next = nullptr;

                // Add the new patient to the linked list
                if (!head) {
                    head = newPatient; // If the list is empty, set as head
                } else {
                    Patient* temp = head;
                    while (temp->next) {
                        temp = temp->next; // Traverse to the end
                    }
                    temp->next = newPatient; // Add to the end
                }
            }
        }
        inFile.close();
    }
};

int main() {
    HospitalManagement hm("patients.txt");
    int choice;
    do {
        cout << "\nHospital Management System\n";
        cout << "1. Add Patient\n";
        cout << "2. Display Patients\n";
        cout << "3. Modify Patient\n";
        cout << "4. Search Patient\n";
        cout << "5. Delete Patient\n";
        cout << "6. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;

        if (cin.fail()) {
            cin.clear(); // Clear the error flag
            cin.ignore(numeric_limits<streamsize>::max(), '\n'); // Discard invalid input
            cout << "Invalid input. Please enter a number." << endl;
            continue; // Skip the rest of the loop
        }

        switch (choice) {
            case 1: {
                Patient p;
                cout << "Enter name: ";
                cin.ignore(); // Clear the newline character from the input buffer
                getline(cin, p.name); // Use getline to allow spaces
                cout << "Enter age: ";
                while (!(cin >> p.age)) {
                    cin.clear(); // Clear the error flag
                    cin.ignore(numeric_limits<streamsize>::max(), '\n'); // Discard invalid input
                    cout << "Invalid age. Please enter a valid number: ";
                }
                cout << "Enter ailment: ";
                cin.ignore(); // Clear the newline character from the input buffer
                getline(cin, p.ailment); // Use getline to allow spaces
                hm.addPatient(p);
                break;
            }
            case 2:
                hm.displayPatients();
                break;
            case 3: {
                string name;
                Patient newDetails;
                cout << "Enter the name of the patient to modify: ";
                cin.ignore();
                getline(cin, name);
                cout << "Enter new name: ";
                getline(cin, newDetails.name);
                cout << "Enter new age: ";
                while (!(cin >> newDetails.age)) {
                    cin.clear();
                    cin.ignore(numeric_limits<streamsize>::max(), '\n');
                    cout << "Invalid age. Please enter a valid number: ";
                }
                cout << "Enter new ailment: ";
                cin.ignore();
                getline(cin, newDetails.ailment);
                hm.modifyPatient(name, newDetails);
                break;
            }
            case 4: {
                string name;
                cout << "Enter the name of the patient to search: ";
                cin.ignore();
                getline(cin, name);
                hm.searchPatient(name);
                break;
            }
            case 5: {
                string name;
                cout << "Enter the name of the patient to delete: ";
                cin.ignore();
                getline(cin, name);
                hm.deletePatient(name);
                break;
            }
            case 6:
                cout << "Exiting the system." << endl;
                break;
            default:
                cout << "Invalid choice. Please try again." << endl;
        }
    } while (choice != 6);

    return 0;
}
