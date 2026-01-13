import React, { useState, useRef, useEffect } from "react";
import Box from "@mui/material/Box";
import Chip from "@mui/material/Chip";
import DragIndicatorIcon from "@mui/icons-material/DragIndicator";

function DraggableItem({
  id,
  data,
  type = "item",
  disabled = false,
  onDragStart,
  onDragEnd,
  children,
  itemProps = {},
}) {
  const ref = useRef(null);

  const handleDragStart = (e) => {
    if (disabled) {
      e.preventDefault();
      return;
    }
    try {
      e.dataTransfer.setData("application/json", JSON.stringify({ id, type }));
    } catch (err) {
      e.dataTransfer.setData("text/plain", id);
    }
    e.dataTransfer.effectAllowed = "move";
    if (onDragStart) onDragStart({ id, data, type });
  };

  const handleDragEndLocal = () => {
    if (onDragEnd) onDragEnd({ id, data, type });
  };

  return (
    <Box
      ref={ref}
      role="listitem"
      draggable={!disabled}
      tabIndex={disabled ? -1 : 0}
      data-id={id}
      data-type={type}
      onDragStart={handleDragStart}
      onDragEnd={handleDragEndLocal}
      data-dnd="item"
      {...itemProps}
    >
      <Box display="flex" alignItems="center" gap={1}>
        <Box aria-hidden="true">
          <DragIndicatorIcon />
        </Box>
        <Box flex={1}>{children}</Box>
      </Box>
    </Box>
  );
}

function DroppableContainer({
  id,
  children = [],
  acceptTypes = ["item"],
  onReorder,
  onDrop,
  onDragStart,
  onDragEnd,
  placeholder = "Drop items here",
  title,
  columnProps = {}, // Внешний контейнер колонки
  listProps = {}, // Список внутри колонки
  titleProps = {}, // Заголовок
  placeholderProps = {}, // Текст "Пусто"
  insertIndicatorProps = {}, // Полоска между элементами
}) {
  const containerRef = useRef(null);
  const [internalChildren, setInternalChildren] = useState(children);
  const [over, setOver] = useState(false);
  const [insertIndex, setInsertIndex] = useState(null);

  useEffect(() => setInternalChildren(children), [children]);

  const getIndexFromPosition = (clientY) => {
    const containerEl = containerRef.current;
    if (!containerEl) return 0;
    const kids = Array.from(containerEl.children).filter(
      (c) => c.dataset && c.dataset.dnd !== "placeholder"
    );
    if (!kids.length) return 0;
    for (let i = 0; i < kids.length; i++) {
      const rect = kids[i].getBoundingClientRect();
      const mid = rect.top + rect.height / 2;
      if (clientY < mid) return i;
    }
    return kids.length;
  };

  const handleDragEnter = (e) => {
    e.preventDefault();
    setOver(true);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    const idx = getIndexFromPosition(e.clientY);
    setInsertIndex(idx);
    if (e.dataTransfer) e.dataTransfer.dropEffect = "move";
  };

  const handleDragLeave = (e) => {
    const current = containerRef.current;
    if (!current) {
      setOver(false);
      return;
    }
    const rect = current.getBoundingClientRect();
    if (
      e.clientX < rect.left ||
      e.clientX > rect.right ||
      e.clientY < rect.top ||
      e.clientY > rect.bottom
    ) {
      setOver(false);
      setInsertIndex(null);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setOver(false);
    let payload = null;
    try {
      payload = JSON.parse(e.dataTransfer.getData("application/json"));
    } catch (err) {
      payload = { id: e.dataTransfer.getData("text/plain") };
    }
    const droppedId = payload?.id;
    const droppedType = payload?.type;

    if (!droppedId || !acceptTypes.includes(droppedType)) {
      setInsertIndex(null);
      return;
    }

    const childArray = React.Children.toArray(internalChildren);
    const existingIndex = childArray.findIndex(
      (child) => child.props && child.props.id === droppedId
    );

    const newIndex = insertIndex === null ? childArray.length : insertIndex;

    if (existingIndex !== -1) {
      // reorder within same container
      if (newIndex !== existingIndex && newIndex !== existingIndex + 1) {
        const newChildren = [...childArray];
        const [removed] = newChildren.splice(existingIndex, 1);
        const insertAt = newIndex > existingIndex ? newIndex - 1 : newIndex;
        newChildren.splice(insertAt, 0, removed);
        setInternalChildren(newChildren);
        if (onReorder) onReorder(newChildren);
      }
    } else {
      // from another container
      if (onDrop) {
        const provided = onDrop({
          id: droppedId,
          type: droppedType,
          targetId: id,
          index: newIndex,
        });
        if (provided) {
          const newChildren = [...childArray];
          newChildren.splice(newIndex, 0, provided);
          setInternalChildren(newChildren);
          if (onReorder) onReorder(newChildren);
        }
      }
    }

    setInsertIndex(null);
  };

  const handleDragStartLocal = (info) => {
    if (onDragStart) onDragStart(info);
  };
  const handleDragEndLocal = (info) => {
    setInsertIndex(null);
    if (onDragEnd) onDragEnd(info);
  };

  const renderedChildren = React.Children.map(internalChildren, (child) => {
    if (child && child.props && child.props.id) {
      return (
        <DraggableItem
          key={child.props.id}
          id={child.props.id}
          data={child.props.data}
          type={child.props.type || "item"}
          onDragStart={handleDragStartLocal}
          onDragEnd={handleDragEndLocal}
          itemProps={{}}
        >
          {child}
        </DraggableItem>
      );
    }
    return child;
  });

  const childElements = React.Children.toArray(renderedChildren).map(
    (child, idx) => {
      const showBefore = insertIndex === idx && over;
      return (
        <Box key={child.key || idx} data-dnd="wrapper">
          {showBefore && (
            <Box data-dnd="insert-indicator" {...insertIndicatorProps} />
          )}
          {child}
        </Box>
      );
    }
  );

  const appendIndicator =
    insertIndex === React.Children.count(internalChildren) && over ? (
      <Box data-dnd="insert-indicator" {...insertIndicatorProps} />
    ) : null;

  return (
    <Box data-dnd="column" {...columnProps}>
      {title ? (
        <Box data-dnd="title" {...titleProps}>
          {title}
        </Box>
      ) : null}
      <Box data-dnd="drop-highlight">
        <Box
          ref={containerRef}
          role="list"
          aria-label={`Droppable list ${id}`}
          onDragEnter={handleDragEnter}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          tabIndex={0}
          data-dnd="container"
          {...listProps}
        >
          {React.Children.count(internalChildren) === 0 ? (
            <Box data-dnd="placeholder" {...placeholderProps}>
              {placeholder}
            </Box>
          ) : (
            <>
              {childElements}
              {appendIndicator}
            </>
          )}
        </Box>
      </Box>

      <div aria-live="polite" hidden />
    </Box>
  );
}

function Draggable({ children, wrapperProps = {} }) {
  const childArray = React.Children.toArray(children).filter(Boolean);

  const [containers, setContainers] = useState(() => {
    const map = {};
    childArray.forEach((child, idx) => {
      const cid = child?.props?.id || `col-${idx}`;
      const childElems = React.Children.toArray(child?.props?.children || []);
      map[cid] = childElems.map((el, j) => {
        const id = el?.props?.id || `${cid}-item-${j}`;
        return { id, element: el, data: el?.props?.data };
      });
    });
    return map;
  });

  const findAndRemove = (id) => {
    let found = null;
    const newMap = {};
    Object.entries(containers).forEach(([cid, items]) => {
      const idx = items.findIndex((it) => it.id === id);
      if (idx !== -1) {
        found = items[idx];
        newMap[cid] = [...items.slice(0, idx), ...items.slice(idx + 1)];
      } else {
        newMap[cid] = items;
      }
    });
    return [found, newMap];
  };

  const handleDrop = ({ id, type, targetId, index }) => {
    const [found, without] = findAndRemove(id);
    if (!found) return null;
    const targetItems = [...(without[targetId] || [])];
    const insertAt = Math.max(0, Math.min(index, targetItems.length));
    targetItems.splice(insertAt, 0, found);
    const newMap = { ...without, [targetId]: targetItems };
    setContainers(newMap);

    // вернуть React-элемент для вставки в DroppableContainer
    return React.cloneElement(found.element, {
      id: found.id,
      data: found.data,
      type: "item",
    });
  };

  const handleReorder = (containerId) => (newChildren) => {
    const ids = newChildren
      .map((ch) => ch.props && ch.props.id)
      .filter(Boolean);
    setContainers((prev) => {
      const items = prev[containerId] || [];
      const lookup = items.reduce((acc, it) => {
        acc[it.id] = it;
        return acc;
      }, {});
      return {
        ...prev,
        [containerId]: ids.map(
          (id) => lookup[id] || { id, element: <Box id={id}>{id}</Box> }
        ),
      };
    });
  };

  return (
    <Box display="flex" gap={2} {...wrapperProps}>
      {childArray.map((child, idx) => {
        const cid = child?.props?.id || `col-${idx}`;
        const title = child?.props?.title || `List ${idx + 1}`;
        const items = containers[cid] || [];
        const childrenForContainer = items.map((it) =>
          React.cloneElement(it.element, { id: it.id, key: it.id })
        );
        return (
          <DroppableContainer
            key={cid}
            id={cid}
            title={title}
            onDrop={handleDrop}
            onReorder={handleReorder(cid)}
          >
            {childrenForContainer}
          </DroppableContainer>
        );
      })}
    </Box>
  );
}

export default function DragAndDropDemo() {
  return (
    <Draggable>
      <DroppableContainer
        id="todo"
        title="To do"
        placeholder="No tasks"
        insertIndicatorProps={{
          sx: { bgcolor: "red", height: "2px", width: "100%" },
        }}
      >
        <Chip id="fix-42" label="Fix bug #42" />
        <Chip id="write-tests" label="Write tests" />
      </DroppableContainer>

      <DroppableContainer
        id="inprogress"
        title="In progress"
        placeholder="Nothing here"
        insertIndicatorProps={{
          sx: { bgcolor: "red", height: "2px", width: "100%" },
        }}
      >
        <Chip id="loading-ui" label="Loading UI" />
      </DroppableContainer>

      <DroppableContainer
        id="done"
        title="Done"
        placeholder="Empty"
        insertIndicatorProps={{
          sx: { bgcolor: "red", height: "2px", width: "100%" },
        }}
      >
        <Chip id="ship-v1" label="Ship v1.0" />
      </DroppableContainer>
    </Draggable>
  );
}
