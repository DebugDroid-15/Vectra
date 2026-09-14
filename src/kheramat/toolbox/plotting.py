from typing import Dict, Callable, Any, Optional
import numpy as np
import re

def _matlab_to_latex(text: str) -> str:
    if not text:
        return text
    if text.startswith("$") and text.endswith("$"):
        return text
    s = text
    s = re.sub(r'\\pi([a-zA-Z]?)', r'\\pi \1', s)
    s = re.sub(r'([a-zA-Z])_([0-9]+)', r'$\1_\2$', s)
    s = re.sub(r'e\^\{([^}]+)\}', r'$e^{\1}$', s)
    if r'\pi' in s and not ('$' in s):
        s = s.replace(r'\pi', r'\pi ')
        s = f"${s}$"
    return s

class PlotManager:
    _instance = None

    def __init__(self):
        self.active_canvas = None
        self.current_axes = None
        self.hold_on = False

    @classmethod
    def get_instance(cls) -> 'PlotManager':
        if cls._instance is None:
            cls._instance = PlotManager()
        return cls._instance

    def set_canvas(self, canvas: Any):
        self.active_canvas = canvas
        self.current_axes = None
        self.hold_on = False

    def get_axes(self):
        if not self.active_canvas:
            return None
        if self.current_axes is None:
            self.current_axes = self.active_canvas.fig.gca()
        return self.current_axes

    def plot(self, *args) -> None:
        ax = self.get_axes()
        if not ax: return
        
        positional = []
        kwargs = {}
        idx = 0
        while idx < len(args):
            arg = args[idx]
            if isinstance(arg, str) or (hasattr(arg, "_array") and arg._array.dtype.kind in ('U', 'S')):
                val_str = str(arg._array.item() if hasattr(arg, "_array") else arg)
                key_lower = val_str.lower()
                if key_lower in ('linewidth', 'lw') and idx + 1 < len(args):
                    lw_val = float(args[idx+1]._array.item() if hasattr(args[idx+1], "_array") else args[idx+1])
                    kwargs['linewidth'] = lw_val
                    idx += 2
                    continue
                elif key_lower in ('color', 'c') and idx + 1 < len(args):
                    c_val = str(args[idx+1]._array.item() if hasattr(args[idx+1], "_array") else args[idx+1])
                    kwargs['color'] = c_val
                    idx += 2
                    continue
                elif key_lower in ('linestyle', 'ls') and idx + 1 < len(args):
                    ls_val = str(args[idx+1]._array.item() if hasattr(args[idx+1], "_array") else args[idx+1])
                    kwargs['linestyle'] = ls_val
                    idx += 2
                    continue
                elif key_lower in ('marker',) and idx + 1 < len(args):
                    m_val = str(args[idx+1]._array.item() if hasattr(args[idx+1], "_array") else args[idx+1])
                    kwargs['marker'] = m_val
                    idx += 2
                    continue
                elif val_str.startswith('-') or val_str in ('r', 'g', 'b', 'k', 'y', 'm', 'c', 'w', 'o', 'x', '+', '*'):
                    positional.append(val_str)
                    idx += 1
                    continue

            if hasattr(arg, "_array"):
                positional.append(arg._array.flatten())
            else:
                positional.append(np.array(arg).flatten())
            idx += 1

    def _refresh(self):
        if self.active_canvas:
            try:
                self.active_canvas.fig.tight_layout()
            except Exception:
                pass
            self.active_canvas.draw()

    def plot(self, *args) -> None:
        ax = self.get_axes()
        if not ax: return
        if not self.hold_on:
            ax.cla()
        
        positional = []
        kwargs = {}
        idx = 0
        while idx < len(args):
            arg = args[idx]
            if isinstance(arg, str) or (hasattr(arg, "_array") and arg._array.dtype.kind in ('U', 'S')):
                val_str = str(arg._array.item() if hasattr(arg, "_array") else arg)
                key_lower = val_str.lower()
                if key_lower in ('linewidth', 'lw') and idx + 1 < len(args):
                    lw_val = float(args[idx+1]._array.item() if hasattr(args[idx+1], "_array") else args[idx+1])
                    kwargs['linewidth'] = lw_val
                    idx += 2
                    continue
                elif key_lower in ('color', 'c') and idx + 1 < len(args):
                    c_val = str(args[idx+1]._array.item() if hasattr(args[idx+1], "_array") else args[idx+1])
                    kwargs['color'] = c_val
                    idx += 2
                    continue
                elif key_lower in ('linestyle', 'ls') and idx + 1 < len(args):
                    ls_val = str(args[idx+1]._array.item() if hasattr(args[idx+1], "_array") else args[idx+1])
                    kwargs['linestyle'] = ls_val
                    idx += 2
                    continue
                elif key_lower in ('marker',) and idx + 1 < len(args):
                    m_val = str(args[idx+1]._array.item() if hasattr(args[idx+1], "_array") else args[idx+1])
                    kwargs['marker'] = m_val
                    idx += 2
                    continue
                elif val_str.startswith('-') or val_str in ('r', 'g', 'b', 'k', 'y', 'm', 'c', 'w', 'o', 'x', '+', '*'):
                    positional.append(val_str)
                    idx += 1
                    continue

            if hasattr(arg, "_array"):
                positional.append(arg._array.flatten())
            else:
                positional.append(np.array(arg).flatten())
            idx += 1

        ax.plot(*positional, **kwargs)
        self._refresh()

    def scatter(self, x, y, *args) -> None:
        ax = self.get_axes()
        if not ax: return
        if not self.hold_on: ax.cla()
        x_arr = x._array.flatten() if hasattr(x, "_array") else np.array(x).flatten()
        y_arr = y._array.flatten() if hasattr(y, "_array") else np.array(y).flatten()
        ax.scatter(x_arr, y_arr, *args)
        self._refresh()

    def bar(self, x, y) -> None:
        ax = self.get_axes()
        if not ax: return
        if not self.hold_on: ax.cla()
        x_arr = x._array.flatten() if hasattr(x, "_array") else np.array(x).flatten()
        y_arr = y._array.flatten() if hasattr(y, "_array") else np.array(y).flatten()
        ax.bar(x_arr, y_arr)
        self._refresh()

    def stem(self, *args) -> None:
        ax = self.get_axes()
        if not ax: return
        if not self.hold_on: ax.cla()
        if len(args) == 1:
            y_arr = args[0]._array.flatten() if hasattr(args[0], "_array") else np.array(args[0]).flatten()
            x_arr = np.arange(len(y_arr))
        else:
            x_arr = args[0]._array.flatten() if hasattr(args[0], "_array") else np.array(args[0]).flatten()
            y_arr = args[1]._array.flatten() if hasattr(args[1], "_array") else np.array(args[1]).flatten()
        ax.stem(x_arr, y_arr)
        self._refresh()

    def xlabel(self, *args) -> None:
        ax = self.get_axes()
        if not ax or not args: return
        text = " ".join(str(a._array.item() if hasattr(a, "_array") and a._array.size == 1 else a) for a in args)
        ax.set_xlabel(text)
        self._refresh()

    def ylabel(self, *args) -> None:
        ax = self.get_axes()
        if not ax or not args: return
        text = " ".join(str(a._array.item() if hasattr(a, "_array") and a._array.size == 1 else a) for a in args)
        ax.set_ylabel(text)
        self._refresh()

    def title(self, *args) -> None:
        ax = self.get_axes()
        if not ax or not args: return
        text = " ".join(str(a._array.item() if hasattr(a, "_array") and a._array.size == 1 else a) for a in args)
        text_clean = _matlab_to_latex(text)
        ax.set_title(text_clean)
        self._refresh()

    def grid(self, flag: str = "on") -> None:
        ax = self.get_axes()
        if not ax: return
        flag_str = str(flag).lower()
        b = flag_str in ("on", "1", "true")
        ax.grid(b)
        self._refresh()

    def figure(self) -> None:
        if not self.active_canvas: return
        self.active_canvas.fig.clf()
        self.current_axes = self.active_canvas.fig.add_subplot(111)
        self._refresh()

    def close(self, *args) -> None:
        if not self.active_canvas: return
        self.active_canvas.fig.clf()
        self.current_axes = None
        self._refresh()

    def subplot(self, *args) -> None:
        if not self.active_canvas or not args: return
        if len(args) == 1:
            raw = args[0]._array.item() if hasattr(args[0], "_array") else args[0]
            val = int(raw)
            if val > 10:
                m, n, p = val // 100, (val % 100) // 10, val % 10
            else:
                m, n, p = val, 1, 1
        elif len(args) >= 3:
            m = int(args[0]._array.item() if hasattr(args[0], "_array") else args[0])
            n = int(args[1]._array.item() if hasattr(args[1], "_array") else args[1])
            p = int(args[2]._array.item() if hasattr(args[2], "_array") else args[2])
        else:
            return
        
        # If starting subplot(M, N, 1), clear figure first if hold is off
        if p == 1 and not self.hold_on:
            self.active_canvas.fig.clf()
            
        self.current_axes = self.active_canvas.fig.add_subplot(m, n, p)
        self._refresh()

    def xlim(self, *args) -> None:
        ax = self.get_axes()
        if not ax or not args: return
        if len(args) == 1 and hasattr(args[0], "_array"):
            lims = args[0]._array.flatten()
            ax.set_xlim([lims[0], lims[1]])
        elif len(args) == 2:
            x1 = float(args[0]._array.item() if hasattr(args[0], "_array") else args[0])
            x2 = float(args[1]._array.item() if hasattr(args[1], "_array") else args[1])
            ax.set_xlim([x1, x2])
        self._refresh()

    def ylim(self, *args) -> None:
        ax = self.get_axes()
        if not ax or not args: return
        if len(args) == 1 and hasattr(args[0], "_array"):
            lims = args[0]._array.flatten()
            ax.set_ylim([lims[0], lims[1]])
        elif len(args) == 2:
            y1 = float(args[0]._array.item() if hasattr(args[0], "_array") else args[0])
            y2 = float(args[1]._array.item() if hasattr(args[1], "_array") else args[1])
            ax.set_ylim([y1, y2])
        self._refresh()

    def text(self, *args) -> None:
        ax = self.get_axes()
        if not ax or len(args) < 3: return
        x = float(args[0]._array.item() if hasattr(args[0], "_array") else args[0])
        y = float(args[1]._array.item() if hasattr(args[1], "_array") else args[1])
        string = " ".join(str(a._array.item() if hasattr(a, "_array") and a._array.size == 1 else a) for a in args[2:])
        string_clean = string.replace(r"\pi", r"$\pi$")
        ax.text(x, y, string_clean)
        self._refresh()

    def gtext(self, *args) -> None:
        ax = self.get_axes()
        if not ax or not args: return
        string = " ".join(str(a._array.item() if hasattr(a, "_array") and a._array.size == 1 else a) for a in args)
        string_clean = _matlab_to_latex(string)

        if not self.active_canvas:
            ax.text(0.95, 0.95, string_clean, transform=ax.transAxes, verticalalignment='top', horizontalalignment='right')
            return

        # Interactive click handler
        canvas = self.active_canvas
        cid = None

        def on_click(event):
            nonlocal cid
            if event.inaxes == ax and event.xdata is not None and event.ydata is not None:
                ax.text(event.xdata, event.ydata, string_clean)
                canvas.draw_idle()
                if cid is not None:
                    canvas.mpl_disconnect(cid)

        cid = canvas.mpl_connect('button_press_event', on_click)

    def zlabel(self, *args) -> None:
        ax = self.get_axes()
        if not ax or not args: return
        text = " ".join(str(a._array.item() if hasattr(a, "_array") and a._array.size == 1 else a) for a in args)
        if hasattr(ax, 'set_zlabel'):
            ax.set_zlabel(text)
        self._refresh()

    def surf(self, X, Y=None, Z=None):
        if not self.active_canvas: return
        if Z is None:
            Z_arr = X._array if hasattr(X, "_array") else np.array(X)
            X_arr, Y_arr = np.meshgrid(np.arange(1, Z_arr.shape[1] + 1), np.arange(1, Z_arr.shape[0] + 1))
        else:
            X_arr = X._array if hasattr(X, "_array") else np.array(X)
            Y_arr = Y._array if hasattr(Y, "_array") else np.array(Y)
            Z_arr = Z._array if hasattr(Z, "_array") else np.array(Z)
        
        self.active_canvas.fig.clf()
        ax = self.active_canvas.fig.add_subplot(111, projection='3d')
        surf_obj = ax.plot_surface(X_arr, Y_arr, Z_arr, cmap='viridis', edgecolor='none')
        self.active_canvas.fig.colorbar(surf_obj, ax=ax, shrink=0.5, aspect=5)
        self.current_axes = ax
        self._refresh()

    def mesh(self, X, Y=None, Z=None):
        if not self.active_canvas: return
        if Z is None:
            Z_arr = X._array if hasattr(X, "_array") else np.array(X)
            X_arr, Y_arr = np.meshgrid(np.arange(1, Z_arr.shape[1] + 1), np.arange(1, Z_arr.shape[0] + 1))
        else:
            X_arr = X._array if hasattr(X, "_array") else np.array(X)
            Y_arr = Y._array if hasattr(Y, "_array") else np.array(Y)
            Z_arr = Z._array if hasattr(Z, "_array") else np.array(Z)
        
        self.active_canvas.fig.clf()
        ax = self.active_canvas.fig.add_subplot(111, projection='3d')
        ax.plot_wireframe(X_arr, Y_arr, Z_arr, color='blue', linewidth=0.5)
        self.current_axes = ax
        self._refresh()

    def quiver(self, X, Y, U, V):
        ax = self.get_axes()
        if not ax: return
        if not self.hold_on: ax.cla()
        x_arr = X._array if hasattr(X, "_array") else np.array(X)
        y_arr = Y._array if hasattr(Y, "_array") else np.array(Y)
        u_arr = U._array if hasattr(U, "_array") else np.array(U)
        v_arr = V._array if hasattr(V, "_array") else np.array(V)
        ax.quiver(x_arr, y_arr, u_arr, v_arr)
        self._refresh()

    def gcf(self):
        return self.active_canvas.fig if self.active_canvas else None

    def gca(self):
        return self.get_axes()

    def close(self, *args) -> None:
        if not self.active_canvas: return
        self.active_canvas.fig.clf()
        self.current_axes = None
        self._refresh()


    def hold(self, flag="on"):
        flag_str = str(flag._array.item() if hasattr(flag, "_array") else flag).lower()
        if flag_str == "on":
            self.hold_on = True
        elif flag_str == "off":
            self.hold_on = False

    def legend(self, *args) -> None:
        ax = self.get_axes()
        if not ax: return
        labels = [str(a._array.item() if hasattr(a, "_array") and a._array.size == 1 else a) for a in args]
        ax.legend(labels)
        self._refresh()

    def plot3(self, *args) -> None:
        ax = self.get_axes()
        if not ax: return
        import matplotlib.pyplot as plt
        if not hasattr(ax, 'plot3D'):
            fig = ax.figure
            fig.delaxes(ax)
            ax = fig.add_subplot(111, projection='3d')
            self.current_axes = ax
        x = args[0]._array if hasattr(args[0], '_array') else args[0]
        y = args[1]._array if hasattr(args[1], '_array') else args[1]
        z = args[2]._array if hasattr(args[2], '_array') else args[2]
        ax.plot3D(x.flatten(), y.flatten(), z.flatten())
        self._refresh()

    def contour3(self, *args) -> None:
        ax = self.get_axes()
        if not ax: return
        import matplotlib.pyplot as plt
        if not hasattr(ax, 'plot3D'):
            fig = ax.figure
            fig.delaxes(ax)
            ax = fig.add_subplot(111, projection='3d')
            self.current_axes = ax
        x = args[0]._array if hasattr(args[0], '_array') else args[0]
        y = args[1]._array if hasattr(args[1], '_array') else args[1]
        z = args[2]._array if hasattr(args[2], '_array') else args[2]
        levels = 10 if len(args) < 4 else int(args[3]._array.item() if hasattr(args[3], '_array') else args[3])
        ax.contour3D(x, y, z, levels)
        self._refresh()
        
    def colorbar(self, *args) -> None:
        ax = self.get_axes()
        if not ax: return
        if len(ax.collections) > 0:
            ax.figure.colorbar(ax.collections[0], ax=ax)
        self._refresh()

    def axis(self, *args) -> None:
        ax = self.get_axes()
        if not ax: return
        if args:
            arg = str(args[0]._array.item() if hasattr(args[0], '_array') else args[0])
            ax.axis(arg)
        self._refresh()

    def view(self, *args) -> None:
        ax = self.get_axes()
        if not ax: return
        if len(args) == 2 and hasattr(ax, 'view_init'):
            az = float(args[0]._array.item() if hasattr(args[0], '_array') else args[0])
            el = float(args[1]._array.item() if hasattr(args[1], '_array') else args[1])
            ax.view_init(elev=el, azim=az)
        self._refresh()

    def shading(self, *args) -> None:
        pass

    def polarplot(self, *args) -> None:
        ax = self.get_axes()
        if not ax: return
        fig = ax.figure
        fig.delaxes(ax)
        ax = fig.add_subplot(111, polar=True)
        self.current_axes = ax
        x = args[0]._array if hasattr(args[0], '_array') else args[0]
        y = args[1]._array if hasattr(args[1], '_array') else args[1]
        ax.plot(x.flatten(), y.flatten())
        self._refresh()

    def histogram(self, *args) -> None:
        ax = self.get_axes()
        if not ax: return
        x = args[0]._array if hasattr(args[0], '_array') else args[0]
        bins = 10 if len(args) < 2 else int(args[1]._array.item() if hasattr(args[1], '_array') else args[1])
        ax.hist(x.flatten(), bins=bins)
        self._refresh()

def km_plot(*args): PlotManager.get_instance().plot(*args)

def km_scatter(x, y, *args): PlotManager.get_instance().scatter(x, y, *args)
def km_bar(x, y): PlotManager.get_instance().bar(x, y)
def km_stem(*args): PlotManager.get_instance().stem(*args)
def km_xlabel(*args): PlotManager.get_instance().xlabel(*args)
def km_ylabel(*args): PlotManager.get_instance().ylabel(*args)
def km_zlabel(*args): PlotManager.get_instance().zlabel(*args)
def km_title(*args): PlotManager.get_instance().title(*args)
def km_grid(flag="on"): PlotManager.get_instance().grid(flag)
def km_figure(): PlotManager.get_instance().figure()
def km_close(*args): PlotManager.get_instance().close(*args)
def km_subplot(*args): PlotManager.get_instance().subplot(*args)
def km_xlim(*args): PlotManager.get_instance().xlim(*args)
def km_ylim(*args): PlotManager.get_instance().ylim(*args)
def km_text(*args): PlotManager.get_instance().text(*args)
def km_gtext(*args): PlotManager.get_instance().gtext(*args)

def km_legend(*args): PlotManager.get_instance().legend(*args)
def km_plot3(*args): PlotManager.get_instance().plot3(*args)
def km_contour3(*args): PlotManager.get_instance().contour3(*args)
def km_colorbar(*args): PlotManager.get_instance().colorbar(*args)
def km_axis(*args): PlotManager.get_instance().axis(*args)
def km_view(*args): PlotManager.get_instance().view(*args)
def km_shading(*args): PlotManager.get_instance().shading(*args)
def km_polarplot(*args): PlotManager.get_instance().polarplot(*args)
def km_histogram(*args): PlotManager.get_instance().histogram(*args)
def km_hold(flag="on"): PlotManager.get_instance().hold(flag)

def km_surf(X, Y=None, Z=None): PlotManager.get_instance().surf(X, Y, Z)
def km_mesh(X, Y=None, Z=None): PlotManager.get_instance().mesh(X, Y, Z)
def km_quiver(X, Y, U, V): PlotManager.get_instance().quiver(X, Y, U, V)
def km_gcf(): return PlotManager.get_instance().gcf()
def km_gca(): return PlotManager.get_instance().gca()

PLOTTING_FUNCTIONS: Dict[str, Callable] = {
    "plot": km_plot,
    "scatter": km_scatter,
    "bar": km_bar,
    "stem": km_stem,
    "xlabel": km_xlabel,
    "ylabel": km_ylabel,
    "zlabel": km_zlabel,
    "title": km_title,
    "legend": km_legend,
    "plot3": km_plot3,
    "contour3": km_contour3,
    "colorbar": km_colorbar,
    "axis": km_axis,
    "view": km_view,
    "shading": km_shading,
    "polarplot": km_polarplot,
    "histogram": km_histogram,
    "hold": km_hold,
    "grid": km_grid,
    "figure": km_figure,
    "close": km_close,
    "subplot": km_subplot,
    "xlim": km_xlim,
    "ylim": km_ylim,
    "text": km_text,
    "gtext": km_gtext,
    "hold": km_hold,
    "surf": km_surf,
    "mesh": km_mesh,
    "quiver": km_quiver,
    "gcf": km_gcf,
    "gca": km_gca,
}
