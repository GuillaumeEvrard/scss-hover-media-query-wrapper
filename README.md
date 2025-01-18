# SCSS Hover Media Query Wrapper

## Description
This Python script automatically wraps all `:hover` blocks in SCSS files with a media query that targets devices capable of hover interactions. It ensures hover effects are only applied on devices like desktops while preventing unintended behavior on touchscreens.

---

## Features
- **Automated scanning**: Recursively scans all `.scss` files in the directory and subdirectories.
- **Smart wrapping**: Identifies and wraps each `:hover` block with the following media query:
  ```scss
  @media (hover: hover) and (pointer: fine) {
    /* Hover styles here */
  }
  ```
- **Preserves structure**: Maintains existing formatting and SCSS structure.
- **Logging**: Logs all inspected files and highlights modified ones for easy tracking.

---

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/scss-hover-media-query-wrapper.git
   ```
2. Navigate to the directory:
   ```bash
   cd scss-hover-media-query-wrapper
   ```

---

## Usage
1. Place the script in the root directory of your SCSS project.
2. Run the script with Python 3:
   ```bash
   python3 hover_media_query_script.py
   ```
3. The script will process all `.scss` files in the directory and subdirectories, wrapping all `:hover` blocks in a media query.

---

## Example

### Input SCSS:
```scss
.button {
  &:hover {
    background-color: #f00;
    color: #fff;
  }
}
```

### Output SCSS:
```scss
.button {
  @media (hover: hover) and (pointer: fine) {
    &:hover {
      background-color: #f00;
      color: #fff;
    }
  }
}
```
