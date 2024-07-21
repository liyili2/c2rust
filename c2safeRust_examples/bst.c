#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int key;
    char* value;
    struct Node* left;
    struct Node* right;
} node_t;

void printAll(node_t* root, int level) {
    if (root->left) {
        printAll(root->left, level+1);
    }
    for (int i = 0; i < level; i++) {
        printf("    ");
    }
    printf("%d:%s\n", root->key, root->value);
    if (root->right) {
        printAll(root->right, level+1);
    }
}

void freeAll(node_t* root) {
    if (root->left) {
        freeAll(root->left);
    }
    if (root->right) {
        freeAll(root->right);
    }
    root->key = 0;
    free(root);
}

void insert(node_t* root, int k, char* v) {
    if (k < root->key) {
        if (root->left) {
            insert(root->left, k, v);
        } else {
            root->left = malloc(sizeof(node_t));
            root->left->key = k;
            root->left->value = v;
            root->left->left = NULL;
            root->left->right = NULL;
        }
    } else if (k > root->key) {
        if (root->right) {
            insert(root->right, k, v);
        } else {
            root->right = malloc(sizeof(node_t));
            root->right->key = k;
            root->right->value = v;
            root->right->left = NULL;
            root->right->right = NULL;
        }
    } else {
        root->value = v;
    }
}

char* search(node_t* root, int k) {
    if (k < root->key) {
        if (root->left) {
            return search(root->left, k);
        } else {
            return NULL;
        }
    } else if (k > root->key) {
        if (root->right) {
            return search(root->right, k);
        } else {
            return NULL;
        }
    } else {
        return root->value;
    }
}

int main(int argc, char* argv[]) {
    node_t* root = malloc(sizeof(node_t));
    root->key = 5;
    root->value = "five";
    root->left = NULL;
    root->right = NULL;
    char* returnholder;
    returnholder = search(root, 5);
    printf("5: %s\n", returnholder);
    returnholder = search(root, 3);
    printf("3: %s\n", returnholder);
    insert(root, 3, "three");
    returnholder = search(root, 3);
    printf("3: %s\n", returnholder);
    returnholder = search(root, 7);
    printf("7: %s\n", returnholder);
    insert(root, 7, "seven");
    returnholder = search(root, 7);
    printf("7: %s\n", returnholder);
    returnholder = search(root, 4);
    printf("4: %s\n", returnholder);
    insert(root, 4, "four");
    returnholder = search(root, 4);
    printf("4: %s\n", returnholder);
    returnholder = search(root, 2);
    printf("2: %s\n", returnholder);
    insert(root, 2, "two");
    returnholder = search(root, 2);
    printf("2: %s\n", returnholder);
    returnholder = search(root, 6);
    printf("6: %s\n", returnholder);
    insert(root, 6, "six");
    returnholder = search(root, 6);
    printf("6: %s\n", returnholder);
    returnholder = search(root, 8);
    printf("8: %s\n", returnholder);
    insert(root, 8, "eight");
    returnholder = search(root, 8);
    printf("8: %s\n", returnholder);
    printAll(root, 0);
    freeAll(root);
}
