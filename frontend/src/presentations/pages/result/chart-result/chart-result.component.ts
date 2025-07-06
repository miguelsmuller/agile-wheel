import { Component, ElementRef, ViewChild, AfterViewInit } from '@angular/core';

import * as echarts from 'echarts/core';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  PolarComponent,
  GraphicComponent,
} from 'echarts/components';
import { BarChart } from 'echarts/charts';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  PolarComponent,
  BarChart,
  GraphicComponent,
  CanvasRenderer,
]);

@Component({
  selector: 'app-chart-result',
  imports: [],
  templateUrl: './chart-result.component.html',
})
export class ChartResultComponent implements AfterViewInit {
  maxValue = 15;

  data = [
    {
      name: 'Pessoas Sensacionais',
      itens: [
        { name: 'Colaboração e comunicação', value: 12 },
        { name: 'Motivação e confiança', value: 9 },
        { name: 'Autonomia e auto-organização', value: 7 },
        { name: 'Melhoria Contínua', value: 11 },
        { name: 'Interdisciplinaridade', value: 13 },
      ],
    },
    {
      name: 'Experimente e Aprenda Rápido',
      itens: [
        { name: 'Compartilhamento de conhecimento', value: 2 },
        { name: 'Comprometimento com o produto', value: 8 },
        { name: 'Práticas Lean-Agile', value: 14 },
        { name: 'Ritmo das entregas', value: 9 },
        { name: 'Granularidade de demandas', value: 12 },
      ],
    },
    {
      name: 'Segurança é um Pré-requisito',
      itens: [
        { name: 'Trabalho sustentável', value: 7 },
        { name: 'Métricas Ágeis', value: 10 },
        { name: 'Estimativas & contratos ágeis', value: 6 },
        { name: 'Metas/ORKs', value: 11 },
        { name: 'Desdobramentos estratégicos', value: 8 },
      ],
    },
    {
      name: 'Valor a Todo Instante',
      itens: [
        { name: 'Discovery/Upstream Kanban', value: 9 },
        { name: 'User Experience (UX/UI)', value: 14 },
        { name: 'Entrega de valor (percebido)', value: 4 },
        { name: 'Relacionamento com o negócio', value: 6 },
        { name: 'Satisfação do cliente', value: 10 },
      ],
    },
  ];

  flatData = this.data.flatMap(group => group.itens);

  labelMap: Record<string, string> = {
    'Colaboração e comunicação': 'Colaboração\ne comunicação',
    'Motivação e confiança': 'Motivação\ne confiança',
    'Autonomia e auto-organização': 'Autonomia\ne auto-organização',
    'Melhoria Contínua': 'Melhoria\nContínua',
    Interdisciplinaridade: 'Interdisciplinaridade',
    'Compartilhamento de conhecimento': 'Compartilhamento\nde conhecimento',
    'Comprometimento com o produto': 'Comprometimento\ncom o produto',
    'Práticas Lean-Agile': 'Práticas\nLean-Agile',
    'Ritmo das entregas': 'Ritmo das\nentregas',
    'Granularidade de demandas': 'Granularidade\nde demandas',
    'Trabalho sustentável': 'Trabalho\nsustentável',
    'Métricas Ágeis': 'Métricas\nÁgeis',
    'Estimativas & contratos ágeis': 'Estimativas\n& contratos ágeis',
    'Metas/ORKs': 'Metas/ORKs',
    'Desdobramentos estratégicos': 'Desdobramentos\nestratégicos',
    'Discovery/Upstream Kanban': 'Discovery/Upstream\nKanban',
    'User Experience (UX/UI)': 'User Experience\n(UX/UI)',
    'Entrega de valor (percebido)': 'Entrega de valor\n(percebido)',
    'Relacionamento com o negócio': 'Relacionamento\ncom o negócio',
    'Satisfação do cliente': 'Satisfação\ndo cliente',
  };

  option = {
    polar: {},
    // Eixo das categorias - giram ao redor do centro
    angleAxis: {
      type: 'category',
      data: this.flatData.map(d => d.name),
      z: 0,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        interval: 0,
        fontSize: 12,
        margin: 10,
        align: 'center',
        formatter: (value: string) => this.labelMap[value] || value,
      },
    },
    // Eixo dos valores - de dentro pra fora
    radiusAxis: {
      max: this.maxValue,
      min: 0,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { show: false },
      splitLine: { show: false },
    },
    series: [
      // Série de fundo (efeito de borda)
      {
        type: 'bar',
        data: Array(this.flatData.length).fill(this.maxValue),
        coordinateSystem: 'polar',
        barGap: '-100%',
        z: -1,
        itemStyle: {
          color: '#e0e0e0',
          borderColor: '#ccc',
          borderWidth: 1,
        },
      },

      // Série principal com cores otimizadas e label destacado
      {
        type: 'bar',
        data: this.flatData.map(d => d.value),
        coordinateSystem: 'polar',
        barCategoryGap: '8%',
        z: 1,
        label: {
          show: true,
          position: 'insideEnd',
          color: '#FFFFFF',
          fontSize: 18,
          fontWeight: 'bold',
          textShadowBlur: 3,
          textShadowOffsetX: 1,
          textShadowOffsetY: 1,
          formatter: '{c}',
        },
        itemStyle: {
          color: (params: { value: number }) => {
            const val = params.value;
            const percent = val / this.maxValue;

            if (percent >= 0.9) return '#2a9d8f';
            if (percent >= 0.7) return '#1f4e5f';
            if (percent >= 0.5) return '#e9c46a';
            if (percent >= 0.3) return '#f4a261';
            return '#e76f51';
          },
        },
      },
    ],
    // Extra Itens
    graphic: [
      {
        type: 'text',
        right: '20',
        top: '50',
        style: {
          text: 'Pessoas\nSensacionais',
          fill: '#444',
          font: 'bold 22px sans-serif',
          textAlign: 'right',
        },
      },
      {
        type: 'text',
        right: '20',
        bottom: '50',
        style: {
          text: 'Experimente e\nAprenda Rápido',
          fill: '#444',
          font: 'bold 22px sans-serif',
          textAlign: 'right',
        },
      },
      {
        type: 'text',
        left: '20',
        bottom: '50',
        style: {
          text: 'Segurança é\num Pré-requisito',
          fill: '#444',
          font: 'bold 22px sans-serif',
          textAlign: 'left',
        },
      },
      {
        type: 'text',
        left: '20',
        top: '50',
        style: {
          text: 'Valor a\nTodo Instante',
          fill: '#444',
          font: 'bold 22px sans-serif',
          textAlign: 'left',
        },
      },

      /* --- LINHA HORIZONTAL --- */
      {
        type: 'line',
        shape: { x1: 0, y1: '50%', x2: '100%', y2: '50%' },
        style: { stroke: '#bbb', lineWidth: 2 },
        silent: true,
        z: 100,
      },
      /* --- LINHA VERTICAL --- */
      {
        type: 'line',
        shape: { x1: '50%', y1: 0, x2: '50%', y2: '100%' },
        style: { stroke: '#bbb', lineWidth: 2 },
        silent: true,
        z: 100,
      },
    ],
  };

  @ViewChild('chartContainer', { static: true })
  chartContainer!: ElementRef<HTMLDivElement>;

  ngAfterViewInit() {
    const chart = echarts.init(this.chartContainer.nativeElement);
    chart.setOption(this.option);
  }
}
