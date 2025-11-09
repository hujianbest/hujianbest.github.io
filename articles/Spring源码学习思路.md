---
title: Spring源码学习思路
date: 2021-11-28 21:40:00
tags: 源码学习
description: Spring源码整体结构和其中最值得阅读的部分。
---

上篇文章*学习源码的三大理由*中提到了如何去阅读源码，今天就如何去阅读Spring的源码做个样例。

首先要说明的是，Spring发展到今天，代码已经非常多了，不建议通读Spring的源码，阅读最核心的，以及工作中密切相关的即可。

## 整体结构

有关Spring框架的介绍可以从[官方文档](https://docs.spring.io/spring-framework/docs/4.0.x/spring-framework-reference/html/overview.html)获得。

Spring 框架由组织成大约 20 个模块的功能组成。这些模块分为Core Container, Data Access/Integration, Web, AOP (Aspect Oriented Programming), Instrumentation, Test。如下图所示![spring-overview](/images/spring-overview.png)

## 核心组成：Core Container

这是Spring最核心的部分，也是Spring的基石。核心容器包含Spring的Core模块、Beans模块、Context模块和SpEL模块。对应到Spring源码中的子模块分别为：

*Core：spring-core*

*Beans：spring-beans*

*Context：spring-context*

*SpEL：spring-expression*

Core和Beans模块提供框架的基本能力，包括IOC和依赖注入。

SpEL是 JSP 2.1 规范中指定的统一表达式语言的扩展。该语言支持设置和获取属性值、属性赋值、方法调用、访问数组的上下文、集合和索引器、逻辑和算术运算符、命名变量以及从 Spring 的 IoC 容器中按名称检索对象。

Context是建立在其他模块基础上的一个上下文模块，它依赖core、beans、spel，此外还依赖aop模块。Context继承了Beans的特征，此外还添加了对国际化、事件、资源加载的支持。

对以上几个模块的代码行做了个统计，可以更好的去做阅读的计划。

| 模块              | 代码行 |
| ----------------- | ------ |
| spring-core       | 46K    |
| spring-beans      | 45K    |
| spring-expression | 11K    |
| spring-context    | 35K    |

这是最建议去学习的几个模块。因为Context中大量使用了AOP，另一个可以顺藤摸瓜去学的模块就是spring-aop，它的代码量如下：

| 模块       | 代码量 |
| ---------- | ------ |
| spring-aop | 12K    |

## 其他组成部分

+ Data Access/Integration：包括 JDBC, ORM, OXM, JMS 和事务模块。

+ Web：包括 Web, Web-Servlet, WebSocket 和Web-Portlet 模块。

+ AOP and Instrumentation

+ Test
