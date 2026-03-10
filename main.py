import flet as ft
import chess

board = chess.Board()

piece_symbols = {
    "P": "♙", "N": "♘", "B": "♗", "R": "♖", "Q": "♕", "K": "♔",
    "p": "♟", "n": "♞", "b": "♝", "r": "♜", "q": "♛", "k": "♚",
}

selected_square = None
legal_squares = []
page_instance = None

def square_to_coords(square):
    return 7 - (square // 8), square % 8

def coords_to_square(row, col):
    return (7 - row) * 8 + col

def build_board():
    if page_instance and page_instance.width and page_instance.height:
        board_size = min(page_instance.width * 0.9, page_instance.height * 0.7)
        square_size = board_size / 8
    else:
        square_size = 60
    
    board_column = ft.Column(
        spacing=0,
        tight=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    for row in range(8):
        board_row = ft.Row(
            spacing=0,
            tight=True,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        for col in range(8):
            square = coords_to_square(row, col)
            piece = board.piece_at(square)
            symbol = piece_symbols.get(piece.symbol(), "") if piece else ""
            
            # Square colors
            color = ft.Colors.WHITE if (row + col) % 2 == 0 else ft.Colors.GREY_400
            
            if square == selected_square:
                color = ft.Colors.YELLOW_200
            elif square in legal_squares:
                color = ft.Colors.GREEN_200
            
            border = None
            if square == selected_square or square in legal_squares:
                border = ft.border.all(2, ft.Colors.BLUE_400)
            
            square_container = ft.Container(
                content=ft.Text(
                    symbol,
                    size=square_size * 0.6,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD,
                ),
                width=square_size,
                height=square_size,
                bgcolor=color,
                alignment=ft.alignment.center,
                border=border,
                on_click=lambda e, s=square: on_square_click(s),
                animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            )
            board_row.controls.append(square_container)
        
        board_column.controls.append(board_row)
    
    return board_column

def on_square_click(square):
    global selected_square, legal_squares, page_instance
    
    piece = board.piece_at(square)
    
    if piece and piece.color == board.turn:
        selected_square = square
        legal_squares = [move.to_square for move in board.legal_moves if move.from_square == square]
    
    elif selected_square is not None and square in legal_squares:
        move = chess.Move(selected_square, square)
        if move in board.legal_moves:
            board.push(move)
        selected_square = None
        legal_squares = []
    
    else:
        selected_square = None
        legal_squares = []
    
    if page_instance:
        page_instance.controls.clear()
        page_instance.add(
            ft.Container(
                content=build_board(),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        page_instance.update()

def page_resize(e):
    if page_instance:
        page_instance.controls.clear()
        page_instance.add(
            ft.Container(
                content=build_board(),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        page_instance.update()

def main(page: ft.Page):
    global page_instance
    page_instance = page
    
    page.title = "Chess Legal Moves Demo"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 10
    
    page.window_width = None
    page.window_height = None
    
    page.on_resized = page_resize
    
    page.add(
        ft.Container(
            content=build_board(),
            alignment=ft.alignment.center,
            expand=True,
        )
    )
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
