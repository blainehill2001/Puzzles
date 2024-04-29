#include <algorithm>
#include <array>
#include <chrono>
#include <iostream>
#include <optional>
#include <set>
#include <utility>
#include <vector>
using namespace std;

/*
board, visited, POSSIBLE_MOVES, sunk all will be arrays of arrays
can't visit square larger than 2 (max sink)
*/
// const int BOARD_SIZE = 4;

const int TIME_CONSTRAINT = 160;     // longest the path can be in time
const int MIN_TIME_CONSTRAINT = 155; // shortest amount of time for valid path
// const int PATH_CONSTRAINT = 38;    // longest the path can be in length

const float TIME_TO_PATH_RATIO = 3.5;
const int NUM_CALLS_TO_SOLVE_PER_PRINT = 1000000;
int calls_count = 0;
const int MAX_VISITED_ALLOWED = 3;

const int MAX_LOWER = 8;
const int BOARD_SIZE = 8;
const int MAX_TIME = 30;
const array<array<int8_t, 3>, 16> POSSIBLE_MOVES_AFTER_SINK = {{{2, 1, 0},
                                                                {1, 2, 0},
                                                                {0, 2, 1},
                                                                {2, 0, 1},
                                                                {1, 0, 2},
                                                                {0, 1, 2},
                                                                {2, -1, 0},
                                                                {-1, 2, 0},
                                                                {-1, 0, 2},
                                                                {0, -1, 2},
                                                                {-2, 1, 0},
                                                                {1, -2, 0},
                                                                {0, -2, 1},
                                                                {-2, 0, 1},
                                                                {-2, -1, 0},
                                                                {-1, -2, 0}}};
const array<array<int8_t, 3>, 24> POSSIBLE_MOVES = {
    {{2, 1, 0},   {1, 2, 0},   {0, 2, 1},   {2, 0, 1},  {0, 2, -1},
     {2, 0, -1},  {1, 0, 2},   {0, 1, 2},   {2, -1, 0}, {-1, 2, 0},
     {1, 0, -2},  {0, 1, -2},  {-1, 0, 2},  {0, -1, 2}, {-2, 1, 0},
     {1, -2, 0},  {-1, 0, -2}, {0, -1, -2}, {0, -2, 1}, {-2, 0, 1},
     {0, -2, -1}, {-2, 0, -1}, {-2, -1, 0}, {-1, -2, 0}}};

inline std::pair<int, int> diametricOpp(const int &i, const int &j) {
  return {BOARD_SIZE - 1 - i, BOARD_SIZE - 1 - j};
}

pair<vector<pair<int, int>>, vector<pair<int, int>>> getChangeSquares(
    const int &i, const int &j,
    const array<array<int, BOARD_SIZE>, BOARD_SIZE> &current_grid) {
  auto d_o = diametricOpp(i, j);
  vector<pair<int, int>> lower, lift;

  for (int x = 0; x < BOARD_SIZE; ++x) {
    for (int y = 0; y < BOARD_SIZE; ++y) {
      if (current_grid[x][y] == current_grid[i][j] &&
          !(d_o.first == x && d_o.second == y))
        lower.push_back({x, y});
    }
  }

  if (current_grid[d_o.first][d_o.second] != current_grid[i][j])
    lift.push_back(d_o);
  return {lower, lift};
}

bool invalid_continue(
    const int &i, const int &j,
    const array<array<int, BOARD_SIZE>, BOARD_SIZE> &visited) {
  return (((i < BOARD_SIZE - 3 && j < BOARD_SIZE - 3) || (i == j)) &&
          visited[0][BOARD_SIZE - 2] == 3 && visited[0][BOARD_SIZE - 3] == 3 &&
          visited[1][BOARD_SIZE - 3] == 3 && visited[1][BOARD_SIZE - 1] == 3 &&
          visited[2][BOARD_SIZE - 3] == 3 && visited[2][BOARD_SIZE - 2] == 3);
}

int get_max_lower(const int &i, const int &j,
                  const array<array<int, BOARD_SIZE>, BOARD_SIZE> &visited,
                  const array<array<int, BOARD_SIZE>, BOARD_SIZE> &grid) {
  int m = grid[i][j] + 2;
  int res = 0;
  for (int x = max(i - 2, 0); x <= min(i + 2, BOARD_SIZE - 1); ++x) {
    for (int y = max(j - 2, 0); y <= min(j + 2, BOARD_SIZE - 1); ++y) {
      int dx = abs(x - i), dy = abs(y - j);
      if (dx != dy && (dx == 0 != dy == 0) &&
          visited[x][y] < MAX_VISITED_ALLOWED && grid[x][y] < grid[i][j]) {
        if (grid[x][y] == grid[i][j])
          return min(MAX_LOWER, m);
        if (max(dx, dy) == 2) {
          res = max(res, grid[i][j] - grid[x][y] + 1);
        } else {
          res = max(res, grid[i][j] - grid[x][y] + 2);
        }
        if (res >= m)
          return m;
      }
    }
  }
  return res;
}

bool in_corner(const int &i, const int &j) {
  if (i >= BOARD_SIZE - 2)
    return j >= BOARD_SIZE - 2;
  else if (i < 4)
    return j < 4;
  return false;
}

optional<pair<vector<pair<int, int>>, int>>
solve(const int &i, const int &j,
      array<array<int, BOARD_SIZE>, BOARD_SIZE> &grid,
      array<array<int, BOARD_SIZE>, BOARD_SIZE> &visited,
      vector<pair<int, int>> &path, int time, set<int> &potential,
      array<array<bool, BOARD_SIZE>, BOARD_SIZE> &has_sunk_grid) {
  ++calls_count;
  if (calls_count % NUM_CALLS_TO_SOLVE_PER_PRINT == 0) {
    // cout << "Path Length: " << path.size() << endl;
    cout << "Grid: " << endl;
    for (int a = 0; a < BOARD_SIZE; ++a) {
      for (int b = 0; b < BOARD_SIZE; ++b) {
        if (a == i && b == j)
          cout << "(" << grid[a][b] << "), ";
        else
          cout << grid[a][b] << ", ";
      }
      cout << "\n";
    }

    cout << endl;
    cout << endl;
    cout << endl;
    // cout << "Visited: " << endl;
    // for (auto &row : visited) {
    //   for (auto num : row)
    //     cout << num << ", ";
    //   cout << endl;
    // }
  }
  if (time >= TIME_CONSTRAINT || in_corner(i, j) ||
      (path.size() > 5 && grid[1][BOARD_SIZE - 1] != 15) ||
      grid[1][BOARD_SIZE - 2] < 13 || //(path.size()>50 && time <
                                      //(TIME_TO_PATH_RATIO+0.2)*path.size())||
      (path.size() > 4 && time < TIME_TO_PATH_RATIO * path.size()))
    return nullopt;
  bool fin = (i == 0 && j == BOARD_SIZE - 1);
  if (fin && time >= MIN_TIME_CONSTRAINT) {
    cout << "Path Length: " << path.size() << endl;
    cout << "Grid: " << endl;
    for (auto &row : grid) {
      for (auto num : row)
        cout << num << ", ";
      cout << endl;
    }
    cout << endl;
    cout << "Visited: " << endl;
    for (auto &row : visited) {
      for (auto num : row)
        cout << num << ", ";
      cout << endl;
    }
    return make_optional(make_pair(path, time));
  } else if (fin)
    return nullopt;
  else if (invalid_continue(i, j, visited))
    return nullopt;

  if (!(path.back().first == BOARD_SIZE - 2 && path.back().second == 0)) {
    set<int> attempt;
    // if last move was a sink, then don't bother checking sink moves
    if (path.back().first < 0) {
      for (const auto &move : POSSIBLE_MOVES_AFTER_SINK) {
        // if path.back().first < 0, then use POSSIBLE_MOVES_AFTER_SINK
        int new_i = i + move[0], new_j = j + move[1], dz = move[2];
        if (0 <= new_i && new_i < BOARD_SIZE && 0 <= new_j &&
            new_j < BOARD_SIZE && visited[new_i][new_j] < MAX_VISITED_ALLOWED &&
            grid[i][j] + dz == grid[new_i][new_j]) {
          int val = new_i * 100 + new_j;
          if (potential.find(val) == potential.end()) {
            attempt.insert(val);
            potential.insert(val);
          }
        }
      }
      // if we get here, then last move was not a sink - therefore use
      // POSSIBLE_MOVES_AFTER_SINK
    } else {
      for (const auto &move : POSSIBLE_MOVES) {
        int new_i = i + move[0], new_j = j + move[1], dz = move[2];
        if (0 <= new_i && new_i < BOARD_SIZE && 0 <= new_j &&
            new_j < BOARD_SIZE && visited[new_i][new_j] < MAX_VISITED_ALLOWED &&
            grid[i][j] + dz == grid[new_i][new_j]) {
          int val = new_i * 100 + new_j;
          if (potential.find(val) == potential.end()) {
            attempt.insert(val);
            potential.insert(val);
          }
        }
      }
    }

    for (const auto &val : attempt) {
      int new_i = val / 100, new_j = val % 100;
      ++visited[new_i][new_j];
      path.push_back({new_i, new_j});
      auto result = solve(new_i, new_j, grid, visited, path, time, potential,
                          has_sunk_grid);
      if (result)
        return result;
      path.pop_back();
      --visited[new_i][new_j];
    }

    if (path.back().first < 0 || grid[i][j] >= 17 || has_sunk_grid[i][j] ||
        (i == BOARD_SIZE - 1 && j == 0))
      return nullopt;
  }

  auto [lower, lift] = getChangeSquares(i, j, grid);
  int n = lower.size();

  set<int> emp;
  int ml = get_max_lower(i, j, visited, grid);
  if (n > 0 && ml > 0) {

    has_sunk_grid[i][j] = true;

    for (short h = 0; h < ml; ++h) {
      for (const auto &[x, y] : lower)
        --grid[x][y];
      if (!lift.empty())
        ++grid[lift[0].first][lift[0].second];

      path.push_back(make_pair(-999, n * (h + 1)));
      auto result = solve(i, j, grid, visited, path, time + n * (h + 1), emp,
                          has_sunk_grid);
      if (result)
        return result;
      path.pop_back();
    }

    for (const auto &[x, y] : lower)
      grid[x][y] += ml;
    if (!lift.empty())
      grid[lift[0].first][lift[0].second] -= ml;
  }

  has_sunk_grid[i][j] = false;

  return nullopt;
}

int main() {

  array<array<int, BOARD_SIZE>, BOARD_SIZE> example_grid = {
      {{11, 10, 11, 14}, {8, 6, 9, 9}, {10, 4, 3, 1}, {7, 6, 5, 0}}};

  array<array<int, BOARD_SIZE>, BOARD_SIZE> real_grid = {
      {{9, 8, 10, 12, 11, 8, 10, 17},
       {7, 9, 11, 9, 10, 12, 14, 12},
       {4, 7, 5, 8, 8, 6, 13, 10},
       {4, 10, 7, 9, 6, 8, 7, 9},
       {2, 6, 4, 2, 5, 9, 8, 11},
       {0, 3, 1, 4, 2, 7, 10, 7},
       {1, 2, 0, 1, 2, 5, 7, 6},
       {0, 2, 4, 3, 5, 6, 2, 4}}};

  array<array<bool, BOARD_SIZE>, BOARD_SIZE> has_sunk_grid = {};
  has_sunk_grid[0][0] = true;

  array<array<int, BOARD_SIZE>, BOARD_SIZE> visited = {};
  ++visited[BOARD_SIZE - 1][0];

  vector<pair<int, int>> path;
  path.push_back(make_pair(BOARD_SIZE - 1, 0));

  int start_i = BOARD_SIZE - 1;
  int start_j = 0;
  int start_time = 0;
  set<int> emp;

  cout << "Starting\n\n";

  auto start = chrono::high_resolution_clock::now();
  auto result = solve(start_i, start_j, real_grid, visited, path, start_time,
                      emp, has_sunk_grid);
  auto stop = chrono::high_resolution_clock::now();
  auto duration = chrono::duration_cast<chrono::milliseconds>(stop - start);

  string letters = "ABCDEFGH";
  if (result) {
    cout << "Solution found!\n";
    cout << "Time: " << result->second << "\n";
    cout << "Path: ";
    for (const auto &p : result->first)
      if (p.first >= 0)
        cout << "(" << letters[p.second] << BOARD_SIZE - p.first << ") -> ";
      else
        cout << "("
             << "Wait"
             << ", " << p.second << ") -> ";
    cout << "End\n";
  } else
    cout << "No solution found.\n";

  cout << "Time taken by solve: " << duration.count() << " milliseconds\n";
  return -1;
}
