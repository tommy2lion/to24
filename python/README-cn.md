# Python 实现：to24

本目录包含 to24 24点游戏求解器的 Python 版本。  
其结构支持多个独立的库（如 `to24`、`hello` 等），并包含用于环境搭建和项目初始化的辅助脚本。

---

## 第一部分 —— 首次使用本软件包

在开始处理本目录下的任何 Python 库之前，你需要先设置一个虚拟环境。  
执行以下命令（请将路径替换为你实际的 `to24/python` 位置）：

```bash
cd /你的路径/to24/python
./tool/setup-python.sh
```

**该脚本的作用：**

- 检测你的 Python 版本（例如 3.14 → `venv314`）
- 创建一个虚拟环境文件夹（例如 `venv314/`）
- 在当前目录生成激活辅助脚本 `activate.sh`
- 配置 VSCode 工作区设置（`.vscode/settings.json`），填入正确的 Python 解释器路径
- 安装 VSCode Python 扩展（如果 `code` 命令可用）

脚本执行完毕后，你的环境已准备就绪，但**尚未激活** – 请继续阅读第二部分。

---

## 第二部分 —— 激活虚拟环境

每次打开新终端进入 `python/` 目录下的任何项目工作时，你都需要激活虚拟环境。

### ✅ 正确的激活方式

```bash
source activate.sh
```

激活后，终端提示符会显示环境名称（例如 `venv314`），并且 `python` 命令将指向虚拟环境内的解释器。

### ❌ 错误的做法
如果你不小心直接执行脚本：

```bash
./activate.sh
```
你会看到错误信息：

```text
❌ Please use `source activate.sh`
```

这是因为直接运行脚本会启动一个**子 shell**，当子 shell 退出时，任何环境变化都会丢失。而使用 `source` 会在**当前 shell** 中执行脚本，从而保留环境设置。

### 🔍 验证激活状态
要确认虚拟环境是否已激活，运行：

```bash
which python
```
输出应显示项目目录内的路径，例如：

```text
/d/code/to24/python/venv314/Scripts/python
```

---

## 第三部分 —— 如何使用 `create-lib.sh`

`tool/create-lib.sh` 脚本可帮助你生成一个具有标准目录结构的新 Python 库项目。  
它会创建一个以库名命名的文件夹，其中包含：

- `examples/` – 一个简单的示例应用程序
- `tests/` – 单元测试模板
- `library_name/` – 实际的 Python 包（仅源代码）
- `setup.py` – 项目根目录下的安装脚本

### 使用示例 —— 创建一个名为 `hello` 的库

```bash
cd /你的路径/to24/python
./tool/create-lib.sh hello
```

执行此命令后，`python/` 目录下将生成以下结构：

```bash
hello/
├── README.md
├── examples/
│   └── app.py*
├── hello/
│   ├── __init__.py
│   ├── algorithm/
│   │   └── __init__.py
│   └── core.py
├── setup.py
└── tests/
    └── test.py*
```

- `hello/examples/app.py` – 使用该库的最小演示程序。
- `hello/tests/test.py` – unittest 测试框架的骨架。
- `hello/hello/` – 实际的包源代码。
- `hello/setup.py` – 库的安装脚本。

然后你可以 `cd hello` 并以可编辑模式安装该库：

```bash
cd hello
pip install -e .
```

现在，只要虚拟环境处于激活状态，你就可以从任何地方导入你的库。

> **注意：** 如果使用名称 `to24` 而不是 `hello`，脚本会生成一个完整的 24 点求解器实现，而不是最小模板。

---

## 第四部分 —— 使用 `install-dev.sh` 进入开发模式

激活虚拟环境（参见第二部分）后，你需要以可编辑模式安装 `to24` 库，以便在导入时能立即反映你的修改。`tool/install-dev.sh` 脚本可以自动完成这一过程。

### 使用方法

只需在 `python/` 目录下的任意位置运行该脚本：

```bash
./tool/install-dev.sh
```

脚本会：
- 保存当前工作目录。
- 切换到 `to24/` 文件夹（其中包含 `setup.py`）。
- 执行 `pip install -e .` 以可编辑模式安装软件包。
- 返回你原先的目录。

如果虚拟环境未激活，脚本会给出警告并要求确认是否继续。

运行此脚本一次后，`to24` 包就注册到了你的虚拟环境中，你可以在任何地方（例如在 `app/` 或 `test/` 中）导入它进行开发。

> **注意：** 每个虚拟环境只需运行一次 `install-dev.sh`，除非你删除了虚拟环境或更改了包名。

---

## 第五部分 —— 使用 `to24` Python 库

激活虚拟环境并通过 `install-dev.sh` 安装包之后，你就可以在自己的代码中使用 `to24` 求解器了。

### 基本用法

```python
from to24 import To24

# 使用默认的 'simple' 算法创建求解器
solver = To24()

# 检查四个数字能否算出 24
result = solver.solve(1, 2, 3, 4)
print(result)  # True

# 同时获取表达式
result, expr = solver.solve(1, 2, 3, 4, return_expr=True)
print(expr)    # ((1 + 2) + 3) + 4
```

### 切换算法

该库支持多种算法。目前已实现：

- `'simple'` – 固定括号模式的穷举算法。
- `'person_like'` – 拟人推理算法的占位符。
- `'remove_dup'` – 去重表达式的占位符。

使用不同算法的方法：

```python
solver = To24(algorithm='person_like')
result = solver.solve(1, 2, 3, 4)   # 目前总是返回 False（占位符）
```

### API 参考

#### `class To24(algorithm='simple')`

- **`solve(a, b, c, d, return_expr=False)`**  
  检查四个整数 `a, b, c, d`（每个介于 1 到 10 之间）能否通过 `+`、`-`、`*`、`/` 运算得到 24。  
  - 如果 `return_expr` 为 `False`（默认），返回一个布尔值。  
  - 如果 `return_expr` 为 `True`，返回一个元组 `(bool, str)`，其中字符串在结果为 `True` 时是一个有效的表达式，否则为空字符串。

### 运行示例

安装完成后，可以运行示例应用：

```bash
cd python/to24
python examples/app.py 1 2 3 4
```

或者运行单元测试：

```bash
python tests/test.py
```