/*
  React Drag & Drop components (single-file demo)
  - DraggableItem: wraps any content and makes it draggable
  - DroppableContainer: accepts draggables, supports reorder within list and transfer between lists
  - Uses HTML5 Drag and Drop API (with a simple keyboard mode)
  - Uses MUI Chip components for demo

  Notes:
  - Install: npm install styled-components @mui/material @mui/icons-material @emotion/react @emotion/styled
  - This file exports default component DragAndDropDemo which demonstrates usage.
*/

import React, { useState, useRef, useEffect } from "react";
import styled from "styled-components";
import Chip from "@mui/material/Chip";
import Avatar from "@mui/material/Avatar";
import DragIndicatorIcon from "@mui/icons-material/DragIndicator";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import WarningIcon from "@mui/icons-material/Warning";

/* ================= Styled components ================= */
const ContainerRow = styled.div`
  display: flex;
  gap: 24px;
  padding: 24px;
  align-items: flex-start;
  background: #f8fafc;
  min-height: 100vh;
`;

const Column = styled.div`
  width: 350px;
  min-height: 200px;
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
`;

const Title = styled.h3`
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #334155;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const List = styled.div`
  background: transparent;
  min-height: 120px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 4px;
`;

const ItemBox = styled.div`
  user-select: none;
  padding: 12px;
  border-radius: 8px;
  background: white;
  border: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: grab;
  transition: all 0.2s ease;

  &:hover {
    border-color: #94a3b8;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  }

  &[aria-grabbed="true"] {
    opacity: 0.7;
    cursor: grabbing;
    transform: scale(0.99) rotate(1deg);
    border-color: #6366f1;
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.15);
    background: #f8fafc;
  }

  &.dragging-over {
    border-color: #6366f1;
    background: #f0f9ff;
  }
`;

const DropHighlight = styled.div`
  position: relative;
  &::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 12px;
    pointer-events: none;
    box-shadow: inset 0 0 0 2px rgba(99, 102, 241, 0.3);
    opacity: 0;
    transition: opacity 0.2s ease;
  }

  &.over::after {
    opacity: 1;
  }
`;

const InsertIndicator = styled.div`
  height: 3px;
  background: linear-gradient(90deg, #6366f1, #8b5cf6);
  margin: 4px 8px;
  border-radius: 3px;
  opacity: 0;
  transform: scaleY(0);
  transition: all 0.2s ease;

  &.visible {
    opacity: 1;
    transform: scaleY(1);
  }
`;

const LiveRegion = styled.div`
  position: absolute;
  left: -9999px;
  width: 1px;
  height: 1px;
  overflow: hidden;
  white-space: nowrap;
`;

const Placeholder = styled.div`
  text-align: center;
  padding: 32px 16px;
  color: #94a3b8;
  font-size: 14px;
  background: #f8fafc;
  border-radius: 8px;
  border: 2px dashed #cbd5e1;
  margin: 4px;
`;

const DragHandle = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  color: #94a3b8;
  cursor: grab;
  border-radius: 4px;

  &:hover {
    background: #f1f5f9;
    color: #64748b;
  }

  & > svg {
    width: 18px;
    height: 18px;
  }
`;

/* ================= DraggableItem ================= */
function DraggableItem({
  id,
  data,
  type = "item",
  disabled = false,
  onDragStart,
  onDragEnd,
  children,
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

    const node = ref.current;
    if (node) {
      const clone = node.cloneNode(true);
      clone.style.boxShadow = "0 12px 32px rgba(0, 0, 0, 0.15)";
      clone.style.padding = "12px";
      clone.style.background = "white";
      clone.style.borderRadius = "8px";
      clone.style.width = `${node.offsetWidth}px`;
      clone.style.opacity = "0.9";
      document.body.appendChild(clone);
      e.dataTransfer.setDragImage(
        clone,
        clone.offsetWidth / 2,
        clone.offsetHeight / 2
      );
      setTimeout(() => document.body.removeChild(clone), 0);
    }
  };

  const handleDragEndLocal = () => {
    if (onDragEnd) onDragEnd({ id, data, type });
  };

  return (
    <ItemBox
      ref={ref}
      role="listitem"
      aria-grabbed={false}
      draggable={!disabled}
      tabIndex={disabled ? -1 : 0}
      data-id={id}
      data-type={type}
      onDragStart={handleDragStart}
      onDragEnd={handleDragEndLocal}
      data-dnd="item"
    >
      <div
        style={{ flex: 1, display: "flex", alignItems: "center", gap: "12px" }}
      >
        <DragHandle>
          <DragIndicatorIcon />
        </DragHandle>
        <div style={{ flex: 1 }}>{children}</div>
      </div>
    </ItemBox>
  );
}

/* ================= DroppableContainer ================= */
function DroppableContainer({
  id,
  children = [], // теперь принимаем массив компонентов
  acceptTypes = ["item"],
  onReorder,
  onDrop,
  onDragStart,
  onDragEnd,
  placeholder = "Drop items here",
  title,
}) {
  const containerRef = useRef(null);
  const [internalChildren, setInternalChildren] = useState(children);
  const [over, setOver] = useState(false);
  const [insertIndex, setInsertIndex] = useState(null);
  const liveRef = useRef(null);

  useEffect(() => setInternalChildren(children), [children]);

  const getIndexFromPosition = (clientY) => {
    const containerEl = containerRef.current;
    const children = Array.from(containerEl.children).filter(
      (c) => c.dataset && c.dataset.dnd !== "placeholder"
    );
    if (!children.length) return 0;

    for (let i = 0; i < children.length; i++) {
      const rect = children[i].getBoundingClientRect();
      const mid = rect.top + rect.height / 2;
      if (clientY < mid) return i;
    }
    return children.length;
  };

  const handleDragEnter = (e) => {
    e.preventDefault();
    setOver(true);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    const dt = e.dataTransfer;
    const idx = getIndexFromPosition(e.clientY);
    setInsertIndex(idx);
    if (dt) dt.dropEffect = "move";
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

    // Получаем индекс элемента среди draggable детей
    const childArray = React.Children.toArray(internalChildren);
    const existingIndex = childArray.findIndex(
      (child) => child.props && child.props.id === droppedId
    );

    const newIndex = insertIndex === null ? childArray.length : insertIndex;

    if (existingIndex !== -1) {
      // Reorder within same container
      if (newIndex !== existingIndex && newIndex !== existingIndex + 1) {
        const newChildren = [...childArray];
        const [removed] = newChildren.splice(existingIndex, 1);
        const insertAt = newIndex > existingIndex ? newIndex - 1 : newIndex;
        newChildren.splice(insertAt, 0, removed);
        setInternalChildren(newChildren);
        if (onReorder) onReorder(newChildren);
      }
    } else {
      // Item from another container
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
        <div key={child.key || idx} data-dnd="wrapper">
          {showBefore && <InsertIndicator className="visible" />}
          {child}
        </div>
      );
    }
  );

  const appendIndicator =
    insertIndex === React.Children.count(internalChildren) && over ? (
      <InsertIndicator className="visible" />
    ) : null;

  return (
    <Column>
      {title && <Title>{title}</Title>}
      <DropHighlight className={over ? "over" : ""}>
        <List
          ref={containerRef}
          role="list"
          aria-label={`Droppable list ${id}`}
          onDragEnter={handleDragEnter}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          tabIndex={0}
          style={over ? { backgroundColor: "rgba(99, 102, 241, 0.02)" } : {}}
          data-dnd="container"
        >
          {React.Children.count(internalChildren) === 0 ? (
            <Placeholder data-dnd="placeholder">{placeholder}</Placeholder>
          ) : (
            <>
              {childElements}
              {appendIndicator}
            </>
          )}
        </List>
      </DropHighlight>
      <LiveRegion aria-live="polite" ref={liveRef} />
    </Column>
  );
}

/* ================= MUI Chip Components ================= */
const CustomChip = ({
  id,
  label,
  color,
  variant = "filled",
  onDelete,
  icon,
  avatar,
}) => (
  <Chip
    id={id}
    label={label}
    color={color}
    variant={variant}
    onDelete={onDelete}
    icon={icon}
    avatar={avatar}
    sx={{
      "& .MuiChip-label": {
        paddingLeft: avatar ? "8px" : "12px",
        paddingRight: onDelete ? "8px" : "12px",
      },
    }}
  />
);

/* ================= Demo usage ================= */
export default function DragAndDropDemo() {
  // Вместо списка объектов теперь список компонентов Chip
  const [listA, setListA] = useState([
    <CustomChip
      key="a1"
      id="a1"
      label="Design System"
      color="primary"
      avatar={<Avatar>DS</Avatar>}
    />,
    <CustomChip
      key="a2"
      id="a2"
      label="In Progress"
      color="warning"
      variant="outlined"
      icon={<WarningIcon />}
    />,
    <CustomChip
      key="a3"
      id="a3"
      label="Completed"
      color="success"
      icon={<CheckCircleIcon />}
    />,
    <CustomChip
      key="a4"
      id="a4"
      label="Frontend Team"
      color="info"
      onDelete={() => console.log("delete")}
    />,
  ]);

  const [listB, setListB] = useState([
    <CustomChip
      key="b1"
      id="b1"
      label="Backend API"
      color="secondary"
      avatar={<Avatar>API</Avatar>}
    />,
    <CustomChip
      key="b2"
      id="b2"
      label="High Priority"
      color="error"
      onDelete={() => console.log("delete")}
    />,
    <CustomChip
      key="b3"
      id="b3"
      label="Documentation"
      color="default"
      variant="outlined"
    />,
  ]);

  const [listC, setListC] = useState([
    <CustomChip
      key="c1"
      id="c1"
      label="Bug Fix"
      color="error"
      variant="outlined"
    />,
    <CustomChip
      key="c2"
      id="c2"
      label="Feature Request"
      color="info"
      variant="outlined"
    />,
  ]);

  const handleDrop = ({ id, targetId, index }) => {
    let movedComponent = null;
    let sourceSetter = null;

    const findComponent = (list, setter) => {
      const component = list.find((comp) => comp.props.id === id);
      if (component) {
        movedComponent = component;
        sourceSetter = setter;
      }
    };

    findComponent(listA, setListA, "A");
    findComponent(listB, setListB, "B");
    findComponent(listC, setListC, "C");

    if (!movedComponent) return null;

    sourceSetter((prev) => prev.filter((comp) => comp.props.id !== id));

    const targetSetters = {
      "list-1": setListA,
      "list-2": setListB,
      "list-3": setListC,
    };

    const setTargetList = targetSetters[targetId];
    if (setTargetList) {
      setTargetList((prev) => {
        const newList = [...prev];
        newList.splice(index, 0, movedComponent);
        return newList;
      });
      return movedComponent;
    }

    return null;
  };

  const handleReorder = (listName, newOrder) => {
    const setters = {
      A: setListA,
      B: setListB,
      C: setListC,
    };
    setters[listName]?.(newOrder);
  };

  return (
    <div style={{ padding: "24px", maxWidth: "1200px", margin: "0 auto" }}>
      <h1 style={{ color: "#1e293b", marginBottom: "8px" }}>
        MUI Chip Drag & Drop
      </h1>
      <p style={{ color: "#64748b", marginBottom: "32px" }}>
        Drag chips between columns or reorder within a column
      </p>

      <ContainerRow>
        <DroppableContainer
          id="list-1"
          children={listA}
          acceptTypes={["item"]}
          onDrop={handleDrop}
          onReorder={(newOrder) => handleReorder("A", newOrder)}
          title="Active Chips"
          placeholder="Drop chips here"
        />

        <DroppableContainer
          id="list-2"
          children={listB}
          acceptTypes={["item"]}
          onDrop={handleDrop}
          onReorder={(newOrder) => handleReorder("B", newOrder)}
          title="In Review"
          placeholder="Drop chips here"
        />

        <DroppableContainer
          id="list-3"
          children={listC}
          acceptTypes={["item"]}
          onDrop={handleDrop}
          onReorder={(newOrder) => handleReorder("C", newOrder)}
          title="Backlog"
          placeholder="Drop chips here"
        />
      </ContainerRow>

      <div
        style={{
          marginTop: "32px",
          padding: "16px",
          background: "#f8fafc",
          borderRadius: "8px",
        }}
      >
        <h4 style={{ marginTop: 0, color: "#475569" }}>How to use:</h4>
        <ul style={{ color: "#64748b", margin: 0, paddingLeft: "20px" }}>
          <li>Drag chips between columns to move them</li>
          <li>Drag within a column to reorder</li>
          <li>Chips with delete icons can be deleted (click the X)</li>
          <li>Visual indicators show drop positions</li>
        </ul>
      </div>
    </div>
  );
}
